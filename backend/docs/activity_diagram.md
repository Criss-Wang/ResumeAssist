@startuml
start
split
    :edit job details;
    if (summarize?) is (<color:red>red) then
        :Summarization;
        :KB search;
    endif
    :persist;
split again
    :edit personal info;
    :persist;
split again
    :edit work experience;
    if (ai assist?) is (<color:red>red) then
        :AI-based Enhancement;
    endif
    :persist;
split again
    :edit project experience;
    if (summarize?) is (<color:red>red) then
        :AI-based Enhancement;
    endif
    :persist;
split again
    :edit skills;
    if (summarize?) is (<color:red>red) then
        :AI-based Enhancement;
    endif
    :persist;
end split
:generate professional summary / self introduction;
:resume compilation;
:post-application feedback collection;
end
@enduml