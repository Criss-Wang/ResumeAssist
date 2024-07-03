@startuml
start
split
    :edit job details;
    if (summarize?) is (yesd) then
        :Summarization;
        :Store to KB;
    endif
    :persist;
split again
    :edit personal info;
    :persist;
split again
    :edit work experience;
    if (ai assist?) is (yes) then
        :AI-based Enhancement;
    endif
    :persist;
split again
    :edit project experience;
    if (ai assist?) is (yes) then
        :AI-based Enhancement;
    endif
    :persist;
split again
    :edit skills;
    if (ai assist?) is (yes) then
        :AI-based Enhancement;
    endif
    :persist;
end split
:generate professional summary / self introduction;
:resume compilation;
:post-application feedback collection;
end
@enduml