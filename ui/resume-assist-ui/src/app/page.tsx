'use client';
import React, { useState } from 'react';
import { Container, Typography, Paper, Box } from '@mui/material';
import Skills from './components/sections/resume-skills'
import SelfIntro from './components/sections/resume-self-intro'
import PersonalInfo from './components/sections/resume-personal-info';
import JobInfo from './components/sections/job-info';
import Projects from './components/sections/resume-projects';
import Experiences from './components/sections/resume-work-experience';
import PDFSection from './components/sections/pdf';
import Researches from './components/sections/resume-research';

export default function Home() {
  const [resume, setResume] = useState({});
  const [job, setJob] = useState({});

  const handleResumeChange = (newResume) => {
    console.log(newResume);
    setResume(newResume);
  };
  const handleJobChange = (newJobInfo) => {
    setJob(newJobInfo);
  };

  return (
   // pages/index.js
      <>
        <div>
          <Container maxWidth={false}  className="flex flex-row items-center justify-center min-h-screen py-8">
            <Typography variant="h2" className="mb-8 text-center">
              Resume Assistant
            </Typography>
            <Box display="flex" justifyContent="space-between" p={2} className="mx-12">
              <Box p={2} flex="1" mr={1} bgcolor="transparent" className="mx-12">
                <JobInfo onJobChange={handleJobChange} job={job}/>
                <Paper elevation={3} className="w-full p-10 m-0" >
                  <Typography variant="h5" className="mb-12 pb-4">
                    Resume Details
                  </Typography>
                  <PersonalInfo onResumeChange={handleResumeChange} resume={resume}/>
                  <Skills onResumeChange={handleResumeChange} resume={resume} job={job}/>
                  <SelfIntro onResumeChange={handleResumeChange} resume={resume} job={job}/>
                  <Experiences onResumeChange={handleResumeChange} resume={resume} job={job}/>
                  <Projects onResumeChange={handleResumeChange} resume={resume} job={job}/>
                  <Researches onResumeChange={handleResumeChange} resume={resume}/>
                </Paper>
              </Box>
              <Box p={2} flex="1" ml={1} bgcolor="transparent" className="mx-12">
                <Paper elevation={3} className="w-full p-10 m-0 min-h-80" >
                  <PDFSection resume={resume}/>
                </Paper>
              </Box>
            </Box>
          </Container>
        </div>
    </>
  );
}