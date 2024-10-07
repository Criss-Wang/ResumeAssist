import os

import click
import numpy as np
import pandas as pd
import textgrad as tg
from dotenv import load_dotenv
from openai import OpenAI
from pandas import DataFrame

from src.utilities.common_utils import set_seed, load_config
from src.tasks import load_task
from src.app.controller import train
from src.app.configs import OptConfig

load_dotenv(override=True)
set_seed(42)

queriesDF = pd.read_csv("datasets/queries/queries.csv", engine="python")


# Read text File
docs = []


def read_text_file(file_path):
    print("loading document " + file_path)
    with open(file_path, "r") as f:
        docs.append(f.read())


# iterate through all files
for file in os.listdir("datasets/kbs"):
    # Check whether file is in text format or not
    if file.endswith(".txt"):
        file_path = f"datasets/kbs/{file}"

        # call read text file function
        read_text_file(file_path)


def docs_to_embeddings(docs: list) -> list:
    openai = OpenAI()
    document_embeddings = []
    for doc in docs:
        response = (
            openai.embeddings.create(input=doc, model="text-embedding-3-small")
            .data[0]
            .embedding
        )
        document_embeddings.append(response)
    return document_embeddings


def get_most_relevant_document(query, articles, article_embeddings):
    openai = OpenAI()
    query_embedding = (
        openai.embeddings.create(input=query, model="text-embedding-3-small")
        .data[0]
        .embedding
    )
    similarities = [
        np.dot(query_embedding, doc_emb)
        / (np.linalg.norm(query_embedding) * np.linalg.norm(doc_emb))
        for doc_emb in article_embeddings
    ]
    # Get the index of the most similar document
    most_relevant_doc_index = np.argmax(similarities)
    # import pdb
    # db.set_trace()
    print(f"doc_index {most_relevant_doc_index}")
    return articles[most_relevant_doc_index]


def optimize(config: OptConfig):
    document_embeddings = docs_to_embeddings(docs)
    print(f"{len(docs)} documents converted to embeddings")

    # write the new csv files.
    indexList = []
    xList = []
    yList = []
    for index, row in queriesDF.iterrows():
        query = row["query"]
        result = row["response"]

        relevant_doc = get_most_relevant_document(query, docs, document_embeddings)

        indexList.append(index)
        xList.append(f"The query is: {query} \n\nThe contexts are: {relevant_doc}")
        yList.append(result)
        print("row added")

    df = pd.DataFrame(data={"id": indexList, "x": xList, "y": yList})
    print("the temporary DataFrame is")
    print(df)

    df.to_csv("datasets/sample/test.csv", index=False)
    df.to_csv("datasets/sample/train.csv", index=False)
    df.to_csv("datasets/sample/val.csv", index=False)

    # load engine
    llm_api_eval = tg.get_engine(engine_name=config.eval_engine_name)
    llm_api_test = tg.get_engine(engine_name=config.test_engine_name)
    tg.set_backward_engine(llm_api_eval, override=True)

    # load data
    train_loader, val_set, test_set, eval_fn, system_prompt = load_task(config)
    print("data loaded")

    # load model & optimizer
    model = tg.BlackboxLLM(llm_api_test, system_prompt)
    optimizer = tg.TextualGradientDescent(
        engine=llm_api_eval, parameters=[system_prompt]
    )
    print("optimizer created")

    # optimize
    results = train(
        train_loader, optimizer, model, eval_fn, system_prompt, val_set, test_set
    )
    print("completed training, final results:")
    print(results)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--config-path", "config_path", type=str, required=True)
def run(config_path: str):
    click.echo("")
    try:
        config = load_config(config_path)
        print("config loaded")
        optimize(config)
    except Exception as e:
        print(f"Failed running benchmark with config: {config_path}")
        print(e)


if __name__ == "__main__":
    cli()
