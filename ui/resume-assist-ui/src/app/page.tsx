'use client';
import { useState } from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import { Container, TextField, Typography, Box, Paper, Chip, IconButton, Button, MenuItem, Select, FormControl, InputLabel } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';

export default function Home() {
  const [skills, setSkills] = useState([[], [], []]);
  const [newSkill, setNewSkill] = useState(['', '', '']);
  const [selfIntro, setSelfIntro] = useState('');
  const [dropdownValue, setDropdownValue] = useState('New');
  const [projects, setProjects] = useState([{ name: '', period: '', descriptions: [] }]);
  const [newDescription, setNewDescription] = useState(['']);


  const handleAddSkill = (index) => {
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
   // pages/index.js
      <>
        <div>
          <Container maxWidth="md" className="flex flex-col items-center justify-center min-h-screen py-8">
            <Typography variant="h2" className="mb-8 text-center">
              Resume Assistant
            </Typography>

            <Paper elevation={3} className="w-full p-4 mt-5 mb-6">
              <Typography variant="h5" className="mb-12 pb-4">
                Job Details
              </Typography>
              <Box component="form" className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex flex-col space-y-4">
                  <TextField label="Job Title" variant="outlined" fullWidth />
                  <TextField label="Company Name" variant="outlined" fullWidth />
                </div>
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
              <Box className="mb-6">
            <Typography variant="h6" className="mb-2">Background</Typography>
            <Box className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex flex-col space-y-4">
                <TextField label="Name" variant="outlined" fullWidth />
                <TextField label="Email" variant="outlined" fullWidth />
                <TextField label="Telephone" variant="outlined" fullWidth />
              </div>
              <div className="flex flex-col space-y-4">
                <TextField label="LinkedIn" variant="outlined" fullWidth />
                <TextField label="GitHub" variant="outlined" fullWidth />
                <TextField label="Personal Website" variant="outlined" fullWidth />
              </div>
            </Box>
          </Box>

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
                  <Button variant="contained" color="primary" onClick={() => handleAddSkill(rowIndex)}>
                    Add
                  </Button>
                </Box>
              </Box>
            ))}
            <Box className="flex gap-4">
              <Button variant="contained" color="primary">Assist</Button>
              <Button variant="contained" color="secondary">Save</Button>
            </Box>
          </Box>

          <Box>
            <Typography variant="h6" className="mb-2">Self-Introduction</Typography>
            <FormControl fullWidth className="mb-4">
              <InputLabel id="self-intro-label">Select</InputLabel>
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
            <TextField
              label="Self-Introduction"
              variant="outlined"
              multiline
              rows={4}
              value={selfIntro}
              onChange={(e) => setSelfIntro(e.target.value)}
              fullWidth
              className="mb-4"
            />
            <Box className="flex gap-4">
              <Button variant="contained" color="primary">Assist</Button>
              <Button variant="contained" color="secondary">Save</Button>
            </Box>
          </Box>
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
                    Add
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
            </Paper>
          </Container>
        </div>
    </>
  );
}