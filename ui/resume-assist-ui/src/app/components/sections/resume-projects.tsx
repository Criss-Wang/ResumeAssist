'use client';
import { useState } from 'react';
import {TextField, Typography, Box, Paper, IconButton, Button} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';

export default function Projects({ onResumeChange, resume, job }) {
    const [projects, setProjects] = useState([{ name: '', period: '', descriptions: [] }]);
    const [newDescription, setNewDescription] = useState(['']);
  
    const handleAddProject = () => {
      setProjects([...projects, { name: '', period: '', descriptions: [] }]);
      setNewDescription([...newDescription, '']);
    };
  
    const handleRemoveProject = (index) => {
      const updatedProjects = [...projects];
      updatedProjects.splice(index, 1);
      setProjects(updatedProjects);
    };
  
    const handleAddDescription = (projectIndex) => {
      const updatedProjects = [...projects];
      const updatednewDescription = [...newDescription];
      if (newDescription[projectIndex].trim() !== '') {
        updatedProjects[projectIndex].descriptions.push(newDescription[projectIndex].trim());
        updatednewDescription[projectIndex] = '';
        setProjects(updatedProjects);
        setNewDescription(updatednewDescription);
      }
    };
  
    const handleRemoveDescription = (projectIndex, descriptionIndex) => {
      const updatedProjects = [...projects];
      updatedProjects[projectIndex].descriptions.splice(descriptionIndex, 1);
      setProjects(updatedProjects);
    };
  
    const handleProjectChange = (projectIndex, field, value) => {
      const updatedProjects = [...projects];
      updatedProjects[projectIndex][field] = value;
      setProjects(updatedProjects);
    };
  
    const handleDescriptionChange = (projectIndex, value) => {
      const updatednewDescription = [...newDescription];
      updatednewDescription[projectIndex] = value;
      console.log(updatednewDescription)
      setNewDescription(updatednewDescription);
    };
    return (
        <Box className="mb-6">
            <Typography variant="h6" className="mb-2">Projects</Typography>
            {projects.map((project, projectIndex) => (
              <Paper key={projectIndex} elevation={2} className="p-4 mb-4">
                <Box className="grid grid-cols-4 gap-4 mb-4">
                  <TextField
                    label="Project Name"
                    variant="outlined"
                    value={project.name}
                    onChange={(e) => handleProjectChange(projectIndex, 'name', e.target.value)}
                    fullWidth
                    className='col-span-3'
                  />
                  <TextField
                    label="Project Period"
                    variant="outlined"
                    value={project.period}
                    onChange={(e) => handleProjectChange(projectIndex, 'period', e.target.value)}
                    fullWidth
                    className='col-span-1'
                  />
                </Box>
                {project.descriptions.map((description, descriptionIndex) => (
                  <Box key={descriptionIndex} className="flex items-center gap-2 mb-2">
                    <TextField
                      label={`Description ${descriptionIndex + 1}`}
                      variant="outlined"
                      value={description}
                      fullWidth
                    />
                    <IconButton onClick={() => handleRemoveDescription(projectIndex, descriptionIndex)}>
                      <CloseIcon />
                    </IconButton>
                  </Box>
                ))}
                <Box className="flex items-center gap-2 mb-4">
                  <TextField
                    label="New Description"
                    variant="outlined"
                    value={newDescription[projectIndex]}
                    onChange={(e) => handleDescriptionChange(projectIndex, e.target.value)}
                    fullWidth
                  />
                  
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={() => handleAddDescription(projectIndex)}
                  >
                    <AddIcon/>
                  </Button>
                </Box>
                <Box className="flex gap-4">
                  <Button variant="contained" color="primary">Assist</Button>
                  <Button variant="contained" color="secondary">Save</Button>
                  <Button variant="contained" color="primary" onClick={handleRemoveProject}>Remove</Button>
                </Box>
              </Paper>
            ))}
            <Button
                variant="contained"
                color="primary"
                startIcon={<AddIcon />}
                onClick={handleAddProject}
            >
                Add Project
            </Button>
        </Box>
    )
}