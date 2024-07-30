'use client';
import { useState } from 'react';
import { TextField, Typography, Box, Paper, IconButton, Button, Divider } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import AddIcon from '@mui/icons-material/Add';
import { green, blue, purple } from "@mui/material/colors"
import axios from "axios";
import RemoveIcon from '@mui/icons-material/Remove';

export default function Experiences({ onResumeChange, resume, job }) {
    const [experiences, setExperiences] = useState([{ id: 1, companyName: '', role: '', startDate: null, endDate: null, location: '', highlights: [] }]);
    const [highlights, setHighlights] = useState([{id: 1, content: ''}]);
    const [editExperienceMode, setEditExperienceMode] = useState<{ experienceId: number | null } | null>(null);
    const [newExperience, setNewExperience] = useState(null);
    const [startDate, setStartDate] = useState<Date | null>(null);
    const [endDate, setEndDate] = useState<Date | null>(null);
    const [isCurrent, setIsCurrent] = useState(false);
  
    const handleAddExperience = () => {
      const newId = experiences.length + 1;
      setExperiences([...experiences, { id: newId, companyName: '', role: '', startDate: null, endDate: null, location: '', highlights: [] }]);
      setHighlights([...highlights, {id: 1, content: ''}]);
    };
  
    const handleRemoveExperience = (experienceId) => {
      setExperiences(experiences.filter(exp => exp.id !== experienceId));
    };
  
    const handleAddHighlight = (experience, highlightContent) => {
      const newHighlightId = experience.highlights.length + 1;
      const newHighlight = { id: newHighlightId, content: highlightContent };
      setExperiences(experiences.map(exp => exp.id === experience.id ? { ...exp, highlights: [...exp.highlights, newHighlight] } : exp));
    };
  
    const handleRemoveHighlight = (experienceId, highlightId) => {
      setExperiences(experiences.map(exp => exp.id === experienceId ? { ...exp, highlights: exp.highlights.filter(h => h.id !== highlightId) } : exp));
    };
  
    const handleEditExperience = (experienceId) => {
      setExperiences(experiences.map(exp => exp.id === experienceId ? newExperience : exp));
    };

    const handleEditNewExperienceField = (field, value) => {
      newExperience[field] = value;
      setNewExperience(newExperience);
    }

    const handleHighlightChange = (experienceId, highlightId, value) => {
      const updatedExperiences = [...experiences];
      updatedExperiences[experienceId].highlights[highlightId].content = value;
      setExperiences(updatedExperiences);
    };

    const handleAssist = async () => {
      console.log(resume, job, experiences);
      try {
          // Send a POST request to your backend
          const response = await fetch('/work/assist', {
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
          work: experiences,
      });
    }

    return (
        <Box className="mb-6">
          <Divider sx={{ borderBottomWidth: '2px'}}/>
          <Box display="flex" className="gap-2" alignItems="center" mb={1}>
            <Typography variant="h6" className="pb-2 pt-4" flexGrow={1}>Work Experiences</Typography>
            <Button
              variant="contained"
              size="small"
              sx={{ 
                backgroundColor: purple[300],
                '&:hover': {
                  backgroundColor: purple[500], // Change color on hover
                },
              }}
              onClick={handleAddExperience}
            >
              <AddIcon/>
            </Button>
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
          {experiences.map(exp => (
            <Box key={exp.id} mb={2}>
              {editExperienceMode?.experienceId === exp.id && (
                <Box mb={2} p={2} sx={{ border: '1px solid #ccc', borderRadius: '4px' }}>
                <Box display="flex" className="gap-2" alignItems="center">
                  <TextField
                      variant='standard'
                      value={newExperience.companyName ?? exp.companyName}
                      onChange={(e) => handleEditNewExperienceField("companyName", e.target.value)}
                      fullWidth
                      multiline
                      size="small"
                      sx={{ flexGrow: 1, mr: 2 }}
                  />
                  <Button
                    variant="contained"
                    color="primary"
                    size="small"
                    className="mr-2"
                    onClick={() => newExperience && handleEditExperience(exp.id)}
                  >
                    Save
                  </Button>
                  <Button
                    variant="contained"
                    color="secondary"
                    size="small"
                    onClick={() => {
                        setEditExperienceMode(null);
                        setNewExperience(null);
                    }}
                  >
                    Cancel
                  </Button>
                </Box>
              </Box>
              )}
            </Box>
          ))}
          {experiences.map(exp => (
            <Paper key={exp.id} elevation={2} className="p-4 mb-4">
              <Typography variant="subtitle1">{exp.companyName || "Company Name"}</Typography>
              <Box className="grid grid-cols-4 gap-4 mb-4">
                <TextField
                  variant="outlined"
                  size="small"
                  value={exp.companyName}
                  disabled
                  fullWidth
                  className='col-span-2'
                />
                <TextField
                  variant="outlined"
                  size="small"
                  value={exp.startDate}
                  disabled
                  fullWidth
                  className='col-span-1'
                />
                <TextField
                  variant="outlined"
                  size="small"
                  value={exp.endDate ?? "Present"}
                  disabled
                  fullWidth
                  className='col-span-1'
                />
              </Box>
            </Paper>
          ))}
            {/* {experiences.map((experience, experienceIndex) => (
              <Paper key={experienceIndex} elevation={2} className="p-4 mb-4">
                <Box className="grid grid-cols-4 gap-4 mb-4">
                  <TextField
                    label="Company Name"
                    variant="outlined"
                    size="small"
                    value={experience.companyName}
                    onChange={(e) => handleExperienceChange(experienceIndex, 'companyName', e.target.value)}
                    fullWidth
                    className='col-span-2'
                  />
                  <TextField
                    label="Period"
                    variant="outlined"
                    size="small"
                    value={experience.period}
                    onChange={(e) => handleExperienceChange(experienceIndex, 'period', e.target.value)}
                    fullWidth
                    className='col-span-1'
                  />
                  
                </Box>
                <TextField
                  label="Role"
                  variant="outlined"
                  value={experience.role}
                  onChange={(e) => handleExperienceChange(experienceIndex, 'role', e.target.value)}
                  fullWidth
                />
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
            ))} */}
        </Box>
    )
}