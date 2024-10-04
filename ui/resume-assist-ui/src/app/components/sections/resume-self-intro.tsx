'use client';
import { useState, useEffect } from 'react';
import { TextField, Typography, Box, Button, MenuItem, Select, FormControl, InputLabel, Divider } from '@mui/material';
import { green, blue } from "@mui/material/colors";
import axios from "axios";

export default function SelfIntro({ onResumeChange, resume, job }) {
  const [selfIntro, setSelfIntro] = useState({ content:'', title: "" });
  const [dropdownValue, setDropdownValue] = useState('Select Version');
  const [selfIntros, setSelfIntros] = useState({ intro_list: [], intro_map: {} });

  useEffect(() => {
    const fetchSelfIntros = async () => {
      try {
        const response = await axios.get('/api/self-intro/all');
        const intro_map = response.data.reduce((acc, item) => {
          acc[item.title] = item.content;
            return acc;
          }, {} as Record<string, string>);
        setSelfIntros({ intro_list: response.data, intro_map: intro_map });
      } catch (error) {
        console.error('Error fetching self-introductions:', error);
      }
    };

    fetchSelfIntros();
  }, []);

  const handleAssist = async () => {
    try {
        console.log({ resume: { ...resume, job_details: job}, intro: selfIntro });
        const response = await fetch('/api/self-intro/assist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ resume: { ...resume, job_details: job}, intro: selfIntro }),
        });
        const result = await response.json();
        setSelfIntro({ ...selfIntro, content: result });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
    } catch (error) {
        console.error('Failed to get intro assist:', error);
    }
  };

  const handleSaveAll = async () => {
    try {
      // Send a POST request to your backend
      const response = await fetch(`/api/self-intro/save/${resume.id}`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ ...selfIntro }),
      });

      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
    } catch (error) {
        console.error('Failed to refresh PDF:', error);
    }
    onResumeChange({
        ...resume,
        self_intro: selfIntro,
    });
  }

  return (
    <Box className="mb-6">
      <Divider sx={{ borderBottomWidth: '2px'}}/>
      <Box display="flex" className="gap-2 mt-1" alignItems="center" mb={1}>
        <Typography variant="h6" className="pb-2 pt-4" flexGrow={1}>Self-Introduction</Typography>
        <Button
          variant="contained"
          size="small"
          sx={{ 
            backgroundColor: blue[300],
            '&:hover': {
              backgroundColor: blue[500], // Change color on hover
            },
          }}
          onClick={handleAssist}
          >
          Assist
        </Button>
        <Button
          variant="contained"
          size="small"
          sx={{ 
            backgroundColor: green[300],
            '&:hover': {
              backgroundColor: green[500], // Change color on hover
            },
          }}
          onClick={handleSaveAll}
          >
          Save
        </Button>
      </Box>
      <div className="mb-3">
        <FormControl className="mb-1 mt-2" fullWidth>
          <Select
            labelId="self-intro-label"
            value={dropdownValue}
            size="small"
            onChange={(e) => {
              setDropdownValue(e.target.value);
              setSelfIntro({ content: selfIntros.intro_map[e.target.value], title: e.target.value });
            }}
            fullWidth
            >
            <MenuItem value="Select Version">Select Version</MenuItem>
            {selfIntros.intro_list.map((intro, idx) => (
              <MenuItem key={idx} value={intro.title}>
                {intro.title}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </div>
      <div className="mb-4">
        <TextField
          label="Self-Introduction"
          variant="outlined"
          multiline
          rows={4}
          value={selfIntro.content}
          onChange={(e) => setSelfIntro({ ...selfIntro, content: e.target.value, title: `${job.company}-${job.position}` })}
          fullWidth
        />
      </div>
    </Box>
  );
}
