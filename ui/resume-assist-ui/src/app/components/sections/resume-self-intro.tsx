'use client';
import { useState } from 'react';
import { TextField, Typography, Box, Button, MenuItem, Select, FormControl, InputLabel } from '@mui/material';

export default function SelfIntro({ onResumeChange, resume, job }) {
  const [selfIntro, setSelfIntro] = useState('');
  const [dropdownValue, setDropdownValue] = useState('New');

  return (
    <Box className="mb-6">
      <Typography variant="h6" className="pb-4 pt-4">Self-Introduction</Typography>
      <div className="mb-4">
        <FormControl className="mb-4 mt-4" fullWidth>
          <InputLabel id="self-intro-label" className="pb-4 pt-4">Select</InputLabel>
          <Select
            labelId="self-intro-label"
            value={dropdownValue}
            onChange={(e) => setDropdownValue(e.target.value)}
            fullWidth
          >
            <MenuItem value="New">New</MenuItem>
            {/* Add more options here */}
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
          className="mb-4 pt-6 pb-4 mt-4"
        />
      </div>
      <Box className="flex gap-4">
        <Button variant="contained" color="primary">Assist</Button>
        <Button variant="contained" color="secondary">Save</Button>
      </Box>
    </Box>
  )
}