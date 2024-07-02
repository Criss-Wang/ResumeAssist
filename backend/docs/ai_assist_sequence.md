@startuml
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
[*] --> fork_state

state RetrievalAgent{
    state Embed {
    }
    state Rank {
    }
    state CrudeFilter {
    }
    state FineFilter ##[dotted]{
    }
}
Embed -> Rank
Rank -> CrudeFilter
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
ReviewerAgent --> [*]: Passed
@enduml