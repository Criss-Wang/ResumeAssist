'use client';
import { Container, Typography, Paper } from '@mui/material';
import Skills from './components/sections/resume-skills'
import SelfIntro from './components/sections/resume-self-intro'
import PersonalInfo from './components/sections/resume-personal-info';
import JobInfo from './components/sections/job-info';
import Projects from './components/sections/resume-projects';
import Experiences from './components/sections/resume-work-experience';

export default function Home() {
  return (
   // pages/index.js
      <>
        <div>
          <Container maxWidth="md" className="flex flex-col items-center justify-center min-h-screen py-8">
            <Typography variant="h2" className="mb-8 text-center">
              Resume Assistant
            </Typography>

            <JobInfo/>

            <Paper elevation={3} className="w-full p-4" >
              <Typography variant="h5" className="mb-12 pb-4">
                Resume Details
              </Typography>
            
              <PersonalInfo/>
              <Skills/>
              <SelfIntro/>
              <Experiences/>
              <Projects/>
              
            </Paper>
          </Container>
        </div>
    </>
  );
}