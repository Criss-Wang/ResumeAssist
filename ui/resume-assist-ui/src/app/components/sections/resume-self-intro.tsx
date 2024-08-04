'use client';
import { useState, useEffect } from 'react';
import { TextField, Typography, Box, Button, MenuItem, Select, FormControl, InputLabel, Divider } from '@mui/material';
import { green, blue } from "@mui/material/colors";
import axios from "axios";

export default function SelfIntro({ onResumeChange, resume, job }) {
  const [selfIntro, setSelfIntro] = useState('');
  const [dropdownValue, setDropdownValue] = useState('Select Version');
  const [selfIntros, setSelfIntros] = useState([]);

  // Fetch available self-introductions from the backend API
  useEffect(() => {
    const fetchSelfIntros = async () => {
      try {
        const response = await axios.get('/api/self-intros'); // Adjust the URL as needed
        setSelfIntros(response.data);
      } catch (error) {
        console.error('Error fetching self-introductions:', error);
      }
    };

    fetchSelfIntros();
  }, []);

  const handleAssist = async () => {
    console.log(resume, job, selfIntro);
    try {
        // Send a POST request to your backend
        const response = await fetch('/self-intro/assist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ resume: resume }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
    } catch (error) {
        console.error('Failed to refresh PDF:', error);
    }
  };

  const handleSaveAll = () => {
    onResumeChange({
        ...resume,
        summary: selfIntro,
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
            onChange={(e) => setDropdownValue(e.target.value)}
            fullWidth
            >
            <MenuItem value="Select Version">Select Version</MenuItem>
            {selfIntros.map((intro) => (
              <MenuItem key={intro.id} value={intro.value}>
                {intro.label}
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
          value={selfIntro}
          onChange={(e) => setSelfIntro(e.target.value)}
          fullWidth
        />
      </div>
    </Box>
  );
}
