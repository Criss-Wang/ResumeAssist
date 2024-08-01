'use client';
import { useState } from 'react';
import { TextField, Typography, Box, Paper, FormGroup,FormControlLabel, IconButton, Button, Divider, Checkbox } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import AddIcon from '@mui/icons-material/Add';
import { Add, Edit, Delete } from '@mui/icons-material';
import { green, blue, purple } from "@mui/material/colors"

export default function Experiences({ onResumeChange, resume, job }) {
    const [experiences, setExperiences] = useState([]);
    const [editExperienceMode, setEditExperienceMode] = useState<{ experienceId: number | null } | null>(null);
    const [newHighlight, setNewHighlight] = useState<{ id: number, hid: number, value: string } | null>(null);
    const [startDate, setStartDate] = useState<Date | null>(null);
    const [endDate, setEndDate] = useState<Date | null>(null);
  
    const handleAddExperience = () => {
      const newId = experiences.length + 1;
      setExperiences([...experiences, { id: newId, companyName: '', role: '', startDate: null, endDate: null, current: false, location: '', highlights: [] }]);
    };
  
    const handleRemoveExperience = (experienceId) => {
      setExperiences(prevExperiences => {
        const filteredExperiences = prevExperiences.filter(exp => exp.id !== experienceId);
        return filteredExperiences.map((exp, index) => ({
          ...exp,
          id: index + 1 // Numbering IDs based on their order in the list
        }));
      });
    };

    const handleExperienceFieldChange = (experienceId, field, value) => {
      setExperiences(experiences.map(exp => exp.id === experienceId ? {...exp, [field]: value} : exp));
    }
  
    const handleAddHighlight = (experience) => {
      const id = experience.highlights.length + 1;
      setExperiences(experiences.map(exp => exp.id === experience.id ? { ...exp, highlights: [...exp.highlights, { id: id, value: "new highlight" }] } : exp));
    };
  
    const handleRemoveHighlight = (experienceId, hId) => {
      setExperiences(experiences.map(exp => exp.id === experienceId ? { ...exp, highlights: exp.highlights.filter(h => h.id !== hId) } : exp));
    };
  
    const handleHighlightChange = () => {
      setExperiences(experiences.map(exp => exp.id === newHighlight.id ? { 
        ...exp, 
        highlights: exp.highlights.map(h => h.id === newHighlight.hid ? { ...h, value: newHighlight.value } : h) 
      } : exp));
      setNewHighlight(null);
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
          <Box display="flex" className="gap-2 mt-1" alignItems="center" mb={1}>
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
                backgroundColor: green[300],
                '&:hover': {
                  backgroundColor: green[500], // Change color on hover
                },
              }}
              onClick={handleSaveAll}
            >
              Save All
            </Button>
          </Box>
          {experiences.length === 0 && (
            <Paper
              elevation={0}
              sx={{
                padding: '25px',
                marginBottom: "20px",
                border: '1.5px solid',
                borderColor: 'grey.400',
                borderRadius: '5px',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '50px',  // Adjust height as needed
                textAlign: 'center'
              }}
            >
              <Typography>
                Add your first work experience
              </Typography>
            </Paper>
          )}
          {experiences.map(exp => (
            <Paper key={exp.id} elevation={2} className="p-4 mb-4">
                <Box display="flex" className="gap-2 mb-0" alignItems="center" mb={1}>
                  <Typography variant="h6" flexGrow={1}>#{exp.id}</Typography>
                  {editExperienceMode?.experienceId !== exp.id && (
                    <>
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
                    </>
                  )}
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
                  disabled={editExperienceMode?.experienceId !== exp.id}
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
                  disabled={editExperienceMode?.experienceId !== exp.id}
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
                      disabled={editExperienceMode?.experienceId !== exp.id}
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
                      disabled={editExperienceMode?.experienceId !== exp.id}
                      fullWidth
                      sx={{
                        '& .MuiInputBase-root.Mui-disabled': {
                          backgroundColor: 'grey.100',
                        },
                      }}
                      className='col-span-3'
                      type="month"
                      onChange={(e) => handleExperienceFieldChange(exp.id, "startDate", e.target.value)}
                    />
                    <TextField
                      variant="outlined"
                      size="small"
                      value={exp.current ? "" : exp.endDate}
                      disabled={editExperienceMode?.experienceId !== exp.id || exp.current}
                      fullWidth
                      sx={{
                        '& .MuiInputBase-root.Mui-disabled': {
                          backgroundColor: 'grey.100',
                        },
                      }}
                      inputProps={{
                        min: exp.startDate // Ensure endDate is after startDate
                      }}
                      className='col-span-3'
                      type="month"
                      onChange={(e) => handleExperienceFieldChange(exp.id, "endDate", e.target.value)}
                    />
                  </Box>
                </Box>
                <Box className="col-span-1 mb-0 pl-0 ml-0">
                  <FormGroup>
                    <FormControlLabel 
                      control={<Checkbox 
                        disabled={editExperienceMode?.experienceId !== exp.id}
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
              {exp.highlights.map((h) => (
                <>
                  {newHighlight?.id === exp.id && newHighlight?.hid === h.id && (
                    <Box mb={2} p={2} sx={{ border: '1px solid #ccc', borderRadius: '4px' }}>
                      <Box display="flex" className="gap-2" alignItems="center">
                        <TextField
                          label="# Edit Highlight"
                          variant='filled'
                          value={newHighlight.value}
                          onChange={(e) => setNewHighlight({ id: newHighlight.id, hid: newHighlight.hid, value: e.target.value })}
                          fullWidth
                          multiline
                          size="small"
                          sx={{ 
                            flexGrow: 1, 
                            mr: 2
                          }}
                          InputProps={{
                            style: {
                              fontSize: '0.9rem',
                              lineHeight: '1.2rem'
                            },
                          }}
                        />
                        <Button
                          variant="contained"
                          color="primary"
                          size="small"
                          className="mr-2"
                          onClick={handleHighlightChange}
                        >
                          Save
                        </Button>
                        <Button
                          variant="contained"
                          color="secondary"
                          size="small"
                          onClick={() => {
                              setNewHighlight(null);
                          }}
                        >
                          Cancel
                        </Button>
                      </Box>
                    </Box>
                  ) }
                  <Box key={h.id} className="flex items-center gap-2 mb-2">
                    <Typography 
                      variant="subtitle1" 
                      flexGrow={1} 
                      sx={{
                        fontSize: '0.9rem',
                        lineHeight: '1.2rem'
                      }}> ⦿  {h.value}
                    </Typography>
                    
                    {editExperienceMode?.experienceId === exp.id && (
                      <IconButton
                        sx = {{
                          width: "15px",
                          height: "15px",
                          '& .MuiSvgIcon-root': {
                            fontSize: '18px', // Adjust the size of the icon
                          },
                        }}
                        onClick={() => setNewHighlight({id: exp.id, hid: h.id, value: h.value})}
                      >
                        <Edit />
                      </IconButton>
                    )}
                    {editExperienceMode?.experienceId == exp.id && (
                      <IconButton 
                        sx = {{
                          width: "15px",
                          height: "15px",
                          '& .MuiSvgIcon-root': {
                            fontSize: '18px', // Adjust the size of the icon
                          },
                        }}
                        onClick={() => handleRemoveHighlight(exp.id, h.id)}
                      >
                        <CloseIcon />
                      </IconButton>
                    )}
                  </Box>
                </>
              ))}
              {editExperienceMode?.experienceId === exp.id && (
                <Box mt={2} display="flex" justifyContent="space-between">
                  <Box flexGrow={1}>
                    <Button
                      variant="outlined"
                      color="primary"
                      size="small"
                      onClick={() => handleAddHighlight(exp)}
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
                      onClick={() => setEditExperienceMode(null)}
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