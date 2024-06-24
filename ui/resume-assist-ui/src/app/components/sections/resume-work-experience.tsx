'use client';
import { useState } from 'react';
import { TextField, Typography, Box, Paper, IconButton, Button } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';

export default function Experiences() {
    const [experiences, setExperiences] = useState([{ companyName: '', period: '', role: "", descriptions: [] }]);
    const [newDescription, setNewDescription] = useState(['']);
  
    const handleAddExperience = () => {
      setExperiences([...experiences, { companyName: '', period: '', role: "", descriptions: [] }]);
      setNewDescription([...newDescription, '']);
    };
  
    const handleRemoveExperience = (index) => {
      const updatedExperiences = [...experiences];
      updatedExperiences.splice(index, 1);
      setExperiences(updatedExperiences);
    };
  
    const handleAddDescription = (experienceIndex) => {
      const updatedExperiences = [...experiences];
      const updatednewDescription = [...newDescription];
      if (newDescription[experienceIndex].trim() !== '') {
        updatedExperiences[experienceIndex].descriptions.push(newDescription[experienceIndex].trim());
        updatednewDescription[experienceIndex] = '';
        setExperiences(updatedExperiences);
        setNewDescription(updatednewDescription);
      }
    };
  
    const handleRemoveDescription = (experienceIndex, descriptionIndex) => {
      const updatedExperiences = [...experiences];
      updatedExperiences[experienceIndex].descriptions.splice(descriptionIndex, 1);
      setExperiences(updatedExperiences);
    };
  
    const handleExperienceChange = (experienceIndex, field, value) => {
      const updatedExperiences = [...experiences];
      updatedExperiences[experienceIndex][field] = value;
      setExperiences(updatedExperiences);
    };
  
    const handleDescriptionChange = (experienceIndex, value) => {
      const updatednewDescription = [...newDescription];
      updatednewDescription[experienceIndex] = value;
      console.log(updatednewDescription)
      setNewDescription(updatednewDescription);
    };
    return (
        <Box className="mb-6">
            <Typography variant="h6" className="mb-2">Work Experiences</Typography>
            {experiences.map((experience, experienceIndex) => (
              <Paper key={experienceIndex} elevation={2} className="p-4 mb-4">
                <Box className="grid grid-cols-4 gap-4 mb-4">
                  <TextField
                    label="Company Name"
                    variant="outlined"
                    value={experience.companyName}
                    onChange={(e) => handleExperienceChange(experienceIndex, 'companyName', e.target.value)}
                    fullWidth
                    className='col-span-1'
                  />
                  <TextField
                    label="Period"
                    variant="outlined"
                    value={experience.period}
                    onChange={(e) => handleExperienceChange(experienceIndex, 'period', e.target.value)}
                    fullWidth
                    className='col-span-1'
                  />
                  <TextField
                    label="Role"
                    variant="outlined"
                    value={experience.role}
                    onChange={(e) => handleExperienceChange(experienceIndex, 'role', e.target.value)}
                    fullWidth
                    className='col-span-2'
                  />
                </Box>
                {experience.descriptions.map((description, descriptionIndex) => (
                  <Box key={descriptionIndex} className="flex items-center gap-2 mb-2">
                    <TextField
                      label={`Description ${descriptionIndex + 1}`}
                      variant="outlined"
                      value={description}
                      fullWidth
                    />
                    <IconButton onClick={() => handleRemoveDescription(experienceIndex, descriptionIndex)}>
                      <CloseIcon />
                    </IconButton>
                  </Box>
                ))}
                <Box className="flex items-center gap-2 mb-4">
                  <TextField
                    label="New Description"
                    variant="outlined"
                    value={newDescription[experienceIndex]}
                    onChange={(e) => handleDescriptionChange(experienceIndex, e.target.value)}
                    fullWidth
                  />
                  
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={() => handleAddDescription(experienceIndex)}
                  >
                    <AddIcon/>
                  </Button>
                </Box>
                <Box className="flex gap-4">
                  <Button variant="contained" color="primary">Assist</Button>
                  <Button variant="contained" color="secondary">Save</Button>
                  <Button variant="contained" color="primary" onClick={handleRemoveExperience}>Remove</Button>
                </Box>
              </Paper>
            ))}
            <Button
                variant="contained"
                color="primary"
                startIcon={<AddIcon />}
                onClick={handleAddExperience}
            >
                Add Experience
            </Button>
        </Box>
    )
}