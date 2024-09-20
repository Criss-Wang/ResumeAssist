'use client';
import { useState } from 'react';
import { TextField, Typography, Checkbox, Box, Paper, IconButton, FormGroup, FormControlLabel, Button, Divider } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import AddIcon from '@mui/icons-material/Add';
import dayjs from 'dayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { MobileDatePicker } from '@mui/x-date-pickers/MobileDatePicker';
import { Add, Edit, Delete } from '@mui/icons-material';
import { green, blue, purple } from "@mui/material/colors"

export default function Projects({ onResumeChange, resume, job }) {
    const [experiences, setExperiences] = useState([]);
    const [editExperienceMode, setEditExperienceMode] = useState<{ experienceId: number | null } | null>(null);
    const [newHighlight, setNewHighlight] = useState<{ id: number, hid: number, value: string } | null>(null);
  
    const handleAddExperience = () => {
      const newId = experiences.length + 1;
      setExperiences([...experiences, { id: newId, projectName: '', startDate: null, endDate: null, url: '', current: false, highlights: [] }]);
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
          projects: experiences,
      });
    }
    

    return (
        <Box className="mb-6">
          <Divider sx={{ borderBottomWidth: '2px'}}/>
          <Box display="flex" className="gap-2 mt-1" alignItems="center" mb={1}>
            <Typography variant="h6" className="pb-2 pt-4" flexGrow={1}>Projects</Typography>
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
                Add your first project
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
              <Box className="grid grid-cols-4 gap-4 mb-4">
                <TextField
                  variant="outlined"
                  size="small"
                  label="Project Name"
                  value={exp.projectName}
                  disabled={editExperienceMode?.experienceId !== exp.id}
                  fullWidth
                  sx={{
                    '& .MuiInputBase-root.Mui-disabled': {
                      backgroundColor: 'grey.100',
                    },
                  }}
                  className='col-span-4'
                  onChange={(e) => handleExperienceFieldChange(exp.id, "projectName", e.target.value)}
                />
              </Box>
              <Box className="grid grid-cols-12 gap-4 mb-2">
                <TextField
                  variant="outlined"
                  size="small"
                  label="Codebase Link"
                  value={exp.url}
                  disabled={editExperienceMode?.experienceId !== exp.id}
                  fullWidth
                  sx={{
                    '& .MuiInputBase-root.Mui-disabled': {
                      backgroundColor: 'grey.100',
                    },
                  }}
                  className='col-span-6'
                  onChange={(e) => handleExperienceFieldChange(exp.id, "url", e.target.value)}
                />
                <LocalizationProvider dateAdapter={AdapterDayjs}>
                  <MobileDatePicker 
                    label="Start Date"
                    disableFuture={true}
                    value={exp.startDate}
                    disabled={editExperienceMode?.experienceId !== exp.id}
                    fullWidth
                    slotProps={{ textField: { size: 'small' } }}
                    sx={{
                      '& .MuiInputBase-root.Mui-disabled': {
                        backgroundColor: 'grey.100',
                      },
                    }}
                    className='col-span-2'
                    maxDate={exp.endDate}
                    format="YYYY/MM"
                    views={['month', 'year']}
                    onChange={(value) => handleExperienceFieldChange(exp.id, "startDate", value)}
                  />
                </LocalizationProvider>
                <LocalizationProvider dateAdapter={AdapterDayjs}>
                  <MobileDatePicker 
                    label="End Date"
                    disableFuture={true}
                    value={exp.current ? null : exp.endDate}
                    disabled={editExperienceMode?.experienceId !== exp.id || exp.current}
                    fullWidth
                    slotProps={{ textField: { size: 'small' } }}
                    sx={{
                      '& .MuiInputBase-root.Mui-disabled': {
                        backgroundColor: 'grey.100',
                      },
                    }}
                    inputProps={{
                      min: exp.startDate // Ensure endDate is after startDate
                    }}
                    minDate={exp.startDate}
                    className='col-span-2 pb-0'
                    format="YYYY/MM"
                    views={['month', 'year']}
                    onChange={(value) => handleExperienceFieldChange(exp.id, "endDate", value)}
                  />
                </LocalizationProvider>
                <FormGroup>
                  <FormControlLabel 
                    control={<Checkbox 
                      disabled={editExperienceMode?.experienceId !== exp.id}
                      checked={exp.current}
                      onChange={(e) => handleExperienceFieldChange(exp.id, "current", e.target.checked)}
                    />} 
                    label={<span className="text-black">Current</span>}
                    labelPlacement="end"
                    sx={{fontcolor: "black"}}
                    className='pl-1'
                  />
                </FormGroup>
              </Box>
              <Typography variant="subtitle1" className='pl-1 mb-2 underline italic'>Highlights</Typography>
              {exp.highlights.map((h) => (
                <>
                  {newHighlight?.id === exp.id && newHighlight?.hid === h.id && (
                    <Box mb={2} p={1} sx={{ border: '1px solid #ccc', borderRadius: '4px' }}>
                      <Box display="flex" className="gap-2 p-0" alignItems="center">
                        <TextField
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
                              paddingTop: '0.3rem',
                              fontSize: '0.9rem',
                              lineHeight: '1rem'
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
                  {(newHighlight?.id !== exp.id || newHighlight?.hid !== h.id) && (<Box key={h.id} className="flex items-center gap-2 mb-2">
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
                  </Box>)}
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
        </Box>
    )
}