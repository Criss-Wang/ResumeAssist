'use client';
import { useState } from 'react';
import { TextField, Typography, Box, Chip, Button, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';

export default function Skills({ onResumeChange, resume, job }) {

    const [skills, setSkills] = useState([[], [], []]);
    const [newSkill, setNewSkill] = useState(['', '', '']);

    const handleAddSkill = (index: number) => {
        if (newSkill[index].trim() !== '') {
          const updatedSkills = [...skills];
          updatedSkills[index].push(newSkill[index].trim());
          setSkills(updatedSkills);
          setNewSkill(['', '', '']);
        }
    };
    
    const handleRemoveSkill = (index, skillIndex) => {
        const updatedSkills = [...skills];
        updatedSkills[index].splice(skillIndex, 1);
        setSkills(updatedSkills);
    };

    return (
        <Box className="mb-6">
            <Typography variant="h6" className="mb-2">Skills</Typography>
            {[0, 1, 2].map((rowIndex) => (
              <Box key={rowIndex} className="mb-4">
                <Box className="flex flex-wrap gap-2 mb-2">
                  {skills[rowIndex].map((skill, skillIndex) => (
                    <Chip
                      key={skillIndex}
                      label={skill}
                      onDelete={() => handleRemoveSkill(rowIndex, skillIndex)}
                      deleteIcon={<CloseIcon />}
                    />
                  ))}
                </Box>
                <Box className="flex items-center gap-2">
                  <TextField
                    label="New Skill"
                    variant="outlined"
                    value={newSkill[rowIndex]}
                    onChange={(e) => {
                      const updatedNewSkill = [...newSkill];
                      updatedNewSkill[rowIndex] = e.target.value;
                      setNewSkill(updatedNewSkill);
                    }}
                    fullWidth
                  />
                  <Button variant="contained" size="small" color="primary" sx={{ width: '1%' }} onClick={() => handleAddSkill(rowIndex)}>
                    <AddIcon/>
                  </Button>
                </Box>
              </Box>
            ))}
            <Box className="flex gap-4">
              <Button variant="contained" color="primary">Assist</Button>
              <Button variant="contained" color="secondary">Save</Button>
            </Box>
        </Box>
    );
}
