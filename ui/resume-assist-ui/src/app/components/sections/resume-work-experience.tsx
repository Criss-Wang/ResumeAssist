'use client';
import { useState } from 'react';
import { TextField, Typography, Box, Paper, FormGroup,FormControlLabel, IconButton, Button, Divider, Checkbox } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import AddIcon from '@mui/icons-material/Add';
import { Add, Edit, Delete } from '@mui/icons-material';
import { green, blue, purple } from "@mui/material/colors"
import axios from "axios";
import RemoveIcon from '@mui/icons-material/Remove';
import exp from 'constants';

export default function Experiences({ onResumeChange, resume, job }) {
    const [experiences, setExperiences] = useState([{ id: 1, companyName: '', role: '', startDate: null, endDate: null, current: false, location: '', highlights: [] }]);
    const [editExperienceMode, setEditExperienceMode] = useState<{ experienceId: number | null } | null>({ experienceId: 1});
    const [newExperience, setNewExperience] = useState(null);
    const [newHighlights, setNewHighlights] = useState("");
    const [startDate, setStartDate] = useState<Date | null>(null);
    const [endDate, setEndDate] = useState<Date | null>(null);
  
    const handleAddExperience = () => {
      const newId = experiences.length + 1;
      setExperiences([...experiences, { id: newId, companyName: '', role: '', startDate: null, endDate: null, current: false, location: '', highlights: [] }]);
    };
  
    const handleRemoveExperience = (experienceId) => {
      setExperiences(experiences.filter(exp => exp.id !== experienceId));
    };

    const handleExperienceFieldChange = (experienceId, field, value) => {
      setExperiences(experiences.map(exp => exp.id === experienceId ? {...exp, [field]: value} : exp));
    }

    const handleExperienceHighlightsChange = (experience, hIdx, value) => {
      // const currHightlights = experience.highlights;
      // currHightlights[hIdx] = value;
      // setExperiences(experiences.map(exp => exp.id === experience.id ? {...exp, highlights: currHightlights} : exp));
    }
  
    const handleAddHighlight = (experienceId) => {
      setExperiences(experiences.map(exp => exp.id === experienceId ? { ...exp, highlights: [...exp.highlights, ""] } : exp));
    };
  
    const handleRemoveHighlight = (experienceId, highlight) => {
      setExperiences(experiences.map(exp => exp.id === experienceId ? { ...exp, highlights: exp.highlights.filter(h => h !== highlight) } : exp));
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
    console.log(experiences);
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
          </Box>
          {experiences.map(exp => (
            <Paper key={exp.id} elevation={2} className="p-4 mb-4">
              <Box display="flex" className="gap-2 mb-0" alignItems="center" mb={2}>
                <Typography variant="h6" flexGrow={1}>#{exp.id}</Typography>
                <IconButton
                  size="small"
                  aria-controls="category-menu"
                  aria-haspopup="true"
                  onClick={() => setEditExperienceMode({ experienceId: exp.id })}
                >
                  <Edit />
                </IconButton>
                <IconButton size="small" onClick={() => handleRemoveExperience(exp.id)}>
                  <Delete />
                </IconButton>
              </Box>
              <Box className="grid grid-cols-4 gap-4 mb-0">
                <Typography variant="subtitle1" className='col-span-2'>Company Name</Typography>
                <Typography variant="subtitle1" className='col-span-2'>Role</Typography>
              </Box>
              <Box className="grid grid-cols-4 gap-4 mb-4">
                <TextField
                  variant="outlined"
                  size="small"
                  value={exp.companyName}
                  disabled={editExperienceMode === null}
                  fullWidth
                  sx={{
                    '& .MuiInputBase-root.Mui-disabled': {
                      backgroundColor: 'grey.100',
                    },
                  }}
                  className='col-span-2'
                  onChange={(e) => handleExperienceFieldChange(exp.id, "companyName", e.target.value)}
                />
                <TextField
                  variant="outlined"
                  size="small"
                  value={exp.role}
                  disabled={editExperienceMode === null}
                  fullWidth
                  sx={{
                    '& .MuiInputBase-root.Mui-disabled': {
                      backgroundColor: 'grey.100',
                    },
                  }}
                  className='col-span-2'
                  onChange={(e) => handleExperienceFieldChange(exp.id, "role", e.target.value)}
                />
              </Box>
              <Box className="grid grid-cols-10 gap-4 mb-2">
                <Box className="col-span-9 gap-4 mb-0">
                  <Box className="grid grid-cols-9 gap-4 mb-0">
                    <Typography variant="subtitle1" className='col-span-3'>Location</Typography>
                    <Typography variant="subtitle1" className='col-span-3'>Start Date</Typography>
                    <Typography variant="subtitle1" className='col-span-3'>End Date</Typography>
                  </Box>
                  <Box className="grid grid-cols-9 gap-4 mb-2">
                    <TextField
                      variant="outlined"
                      size="small"
                      value={exp.location}
                      disabled={editExperienceMode === null}
                      fullWidth
                      sx={{
                        '& .MuiInputBase-root.Mui-disabled': {
                          backgroundColor: 'grey.100',
                        },
                      }}
                      className='col-span-3'
                      onChange={(e) => handleExperienceFieldChange(exp.id, "location", e.target.value)}
                    />
                    <TextField
                      variant="outlined"
                      size="small"
                      value={exp.startDate}
                      disabled={editExperienceMode === null}
                      fullWidth
                      sx={{
                        '& .MuiInputBase-root.Mui-disabled': {
                          backgroundColor: 'grey.100',
                        },
                      }}
                      className='col-span-3'
                      onChange={(e) => handleExperienceFieldChange(exp.id, "startDate", e.target.value)}
                    />
                    <TextField
                      variant="outlined"
                      size="small"
                      value={exp.current ? "" : exp.endDate}
                      disabled={editExperienceMode === null || exp.current}
                      fullWidth
                      sx={{
                        '& .MuiInputBase-root.Mui-disabled': {
                          backgroundColor: 'grey.100',
                        },
                      }}
                      className='col-span-3'
                      onChange={(e) => handleExperienceFieldChange(exp.id, "endDate", e.target.value)}
                    />
                  </Box>
                </Box>
                <Box className="col-span-1 mb-0 pl-0 ml-0">
                  <FormGroup>
                    <FormControlLabel 
                      control={<Checkbox 
                        disabled={editExperienceMode === null}
                        checked={exp.current}
                        onChange={(e) => handleExperienceFieldChange(exp.id, "current", e.target.checked)}
                      />} 
                      label={<span className="text-black">Current</span>}
                      labelPlacement="top"
                      sx={{fontcolor: "black"}}
                      className='ml-0'
                    />
                  </FormGroup>
                </Box>
              </Box>
              <Typography variant="subtitle1" className='mb-2'>Highlights</Typography>
              {exp.highlights.map((h, idx) => (
                <Box key={idx} className="flex items-center gap-2 mb-2">
                  <TextField
                    variant="outlined"
                    size="small"
                    value={h || newHighlights}
                    disabled={editExperienceMode === null}
                    fullWidth
                    sx={{
                      '& .MuiInputBase-root.Mui-disabled': {
                        backgroundColor: 'grey.100',
                      },
                    }}
                    multiline
                    // onChange={(e) => handleExperienceHighlightsChange(exp, idx, e.target.value)}
                    onChange={(e) => setNewHighlights(e.target.value)}
                    />
                  {editExperienceMode?.experienceId && (
                    <IconButton onClick={() => handleRemoveHighlight(exp.id, h)}>
                      <CloseIcon />
                    </IconButton>
                  )}
                </Box>
              ))}
              {editExperienceMode?.experienceId && (
                <Box mt={2} display="flex" justifyContent="space-between">
                  <Box flexGrow={1}>
                    <Button
                      variant="outlined"
                      color="primary"
                      size="small"
                      onClick={() => handleAddHighlight(exp.id)}
                      startIcon={<Add />}
                    >
                      Add Highlight
                    </Button>
                  </Box>
                  <Box display="flex" justifyContent="flex-end" flexGrow={1}>
                    <Button
                      variant="contained"
                      size="small"
                      sx={{
                        backgroundColor: blue[300],
                        '&:hover': {
                          backgroundColor: blue[500], // Change color on hover
                        },
                        ml: 2, // Add margin-left to create space between buttons
                      }}
                      onClick={handleAssist}
                    >
                      Assist
                    </Button>
                    <Button
                      variant="contained"
                      color="primary"
                      size="small"
                      sx={{ 
                        ml: 1,
                        backgroundColor: green[300],
                        '&:hover': {
                          backgroundColor: green[500], // Change color on hover
                        },
                      }}
                      onClick={() => newExperience && handleSaveAll()}
                    >
                      Save
                    </Button>
                  </Box>
                </Box>
              )}
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