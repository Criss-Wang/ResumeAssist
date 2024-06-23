// pages/index.js
import * as React from 'react';
import Head from 'next/head';
import { Container, TextField, Typography, Box, Paper } from '@mui/material';

export default function Home() {
  return (
    <div>
      <Head>
        <title>Resume Assistant</title>
      </Head>
      <Container maxWidth="md" className="flex flex-col items-center justify-center min-h-screen py-8">
        <Typography variant="h2" className="mb-8 text-center">
          Resume Assistant
        </Typography>

        <Paper elevation={3} className="w-full p-4 mb-6">
          <Typography variant="h5" className="mb-4">
            Job Details
          </Typography>
          <Box component="form" className="flex flex-col space-y-4">
            <TextField label="Job Title" variant="outlined" fullWidth />
            <TextField label="Company Name" variant="outlined" fullWidth />
            <TextField
              label="Job Description"
              variant="outlined"
              multiline
              rows={4}
              fullWidth
            />
          </Box>
        </Paper>

        <Paper elevation={3} className="w-full p-4">
          <Typography variant="h5" className="mb-4">
            Resume Section
          </Typography>
          {/* Add Resume Section Content Here */}
        </Paper>
      </Container>
    </div>
  );
}
