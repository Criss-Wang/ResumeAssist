@startuml
state FormatterAgent{
}
FormatterAgent: Align w.t. format requirements
state RendererAgent {
}
RendererAgent: Rendering tasks
state SyncingAgent ##[dotted]{
}
SyncingAgent: Update job platforms
state AI_Assist_Flow {
}
AI_Assist_Flow: Re-run RAG

[*] --> FormatterAgent
FormatterAgent --> AI_Assist_Flow
AI_Assist_Flow --> FormatterAgent
FormatterAgent --> RendererAgent
RendererAgent --> SyncingAgent: Optional
SyncingAgent --> [*]
@enduml