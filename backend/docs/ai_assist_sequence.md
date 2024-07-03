@startuml
title
 Agent-based AI Assist Workflow
end title

state Request {
}

state fork_state <<fork>>
state KeywordExtractionAgent {
    state NER {
    }
    state Filter {
    }
}
NER -> Filter
NER: From job summary
Filter: Top K
Request --> fork_state

state RetrievalAgent{
    state Embed {
    }
    state Ranking {
    }
    state CrudeFilter {
    }
    state FineFilter ##[dotted]{
    }
}
Embed -> Ranking
Ranking -> CrudeFilter
CrudeFilter --> FineFilter: Optional

Embed: From job summary and/or input
CrudeFilter: Top K
FineFilter: Chunk with positive labels


fork_state --> KeywordExtractionAgent
fork_state --> RetrievalAgent


state join_state <<join>>
KeywordExtractionAgent --> join_state: Keywords
RetrievalAgent --> join_state: Resume Chunks

state EnhancerAgent {
    state PromptBuilder {
    }
    state Engine {
    }
}
state ReviewerAgent {
}
ReviewerAgent: Critique
PromptBuilder -> Engine
PromptBuilder: [Optional] in-context learning
Engine: LangChain-based Inference
join_state --> EnhancerAgent: All contexts
EnhancerAgent --> ReviewerAgent
ReviewerAgent --> join_state: Failed. Review provided.
ReviewerAgent --> Response: Passed
@enduml