'use client';
import { useState } from 'react';
import { TextField, Typography, Box, Paper, FormGroup,FormControlLabel, IconButton, Button, Divider, Checkbox } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import AddIcon from '@mui/icons-material/Add';
import { Add, Edit, Delete } from '@mui/icons-material';
import { green, blue, purple } from "@mui/material/colors"


{/* setExperiences([...experiences, { id: newId, institution: '', area: '', degree: '', startDate: null, endDate: null, area: '', highlights: '' }]); */}


export default function Education({ onResumeChange, resume }) {
    const [experiences, setExperiences] = useState([]);
    const [editExperienceMode, setEditExperienceMode] = useState<{ experienceId: number | null } | null>(null);
  
    const handleAddExperience = () => {
      const newId = experiences.length + 1;
      setExperiences([...experiences, { id: newId, institution: '', area: '', degree: '', startDate: null, endDate: null, current: false, area: '', courses: '', gpa: '', other: '' }]);
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
  
    const handleSaveAll = () => {
      onResumeChange({
          ...resume,
          education: experiences,
      });
    }
    

    return (
        <Box className="mb-6">
          <Divider sx={{ borderBottomWidth: '2px'}}/>
          <Box display="flex" className="gap-2 mt-1" alignItems="center" mb={1}>
            <Typography variant="h6" className="pb-2 pt-4" flexGrow={1}>Education</Typography>
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
                Add your first education 
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
                <Typography variant="subtitle1" className='col-span-3'>Institution</Typography>
                <Typography variant="subtitle1" className='col-span-1'>Degree</Typography>
              </Box>
              <Box className="grid grid-cols-4 gap-4 mb-4">
                <TextField
                  variant="outlined"
                  size="small"
                  value={exp.institution}
                  disabled={editExperienceMode?.experienceId !== exp.id}
                  fullWidth
                  sx={{
                    '& .MuiInputBase-root.Mui-disabled': {
                      backgroundColor: 'grey.100',
                    },
                  }}
                  className='col-span-3'
                  onChange={(e) => handleExperienceFieldChange(exp.id, "institution", e.target.value)}
                />
                <TextField
                  variant="outlined"
                  size="small"
                  value={exp.degree}
                  disabled={editExperienceMode?.experienceId !== exp.id}
                  fullWidth
                  sx={{
                    '& .MuiInputBase-root.Mui-disabled': {
                      backgroundColor: 'grey.100',
                    },
                  }}
                  className='col-span-1'
                  onChange={(e) => handleExperienceFieldChange(exp.id, "degree", e.target.value)}
                />
              </Box>
              <Box className="grid grid-cols-10 gap-4 mb-2">
                <Box className="col-span-9 gap-4 mb-0">
                  <Box className="grid grid-cols-9 gap-4 mb-0">
                    <Typography variant="subtitle1" className='col-span-5'>Major</Typography>
                    <Typography variant="subtitle1" className='col-span-2'>Start Date</Typography>
                    <Typography variant="subtitle1" className='col-span-2'>End Date (Expected)</Typography>
                  </Box>
                  <Box className="grid grid-cols-9 gap-4 mb-2">
                    <TextField
                      variant="outlined"
                      size="small"
                      value={exp.area}
                      disabled={editExperienceMode?.experienceId !== exp.id}
                      fullWidth
                      sx={{
                        '& .MuiInputBase-root.Mui-disabled': {
                          backgroundColor: 'grey.100',
                        },
                      }}
                      className='col-span-5'
                      onChange={(e) => handleExperienceFieldChange(exp.id, "area", e.target.value)}
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
                      className='col-span-2'
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
                      className='col-span-2'
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
              <Box className="grid grid-cols-8 gap-4 mb-0">
                <Typography variant="subtitle1" className='col-span-1'>GPA</Typography>
                <Typography variant="subtitle1" className='col-span-7'>Courseworks</Typography>
              </Box>
              <Box className="grid grid-cols-8 gap-4 mb-4">
                <TextField
                  variant="outlined"
                  size="small"
                  value={exp.gpa}
                  disabled={editExperienceMode?.experienceId !== exp.id}
                  fullWidth
                  sx={{
                    '& .MuiInputBase-root.Mui-disabled': {
                      backgroundColor: 'grey.100',
                    },
                  }}
                  className='col-span-1'
                  onChange={(e) => handleExperienceFieldChange(exp.id, "gpa", e.target.value)}
                />
                <TextField
                  variant="outlined"
                  size="small"
                  value={exp.courses}
                  disabled={editExperienceMode?.experienceId !== exp.id}
                  fullWidth
                  sx={{
                    '& .MuiInputBase-root.Mui-disabled': {
                      backgroundColor: 'grey.100',
                    },
                  }}
                  className='col-span-7'
                  onChange={(e) => handleExperienceFieldChange(exp.id, "courses", e.target.value)}
                />
              </Box>
              <Box className="grid grid-cols-4 gap-4 mb-0">
                <Typography variant="subtitle1" className='col-span-4'>Other Highlights (split by ";" sign)</Typography>
              </Box>
              <Box className="grid grid-cols-4 gap-4 mb-4">
                <TextField
                  variant="outlined"
                  size="small"
                  value={exp.other}
                  disabled={editExperienceMode?.experienceId !== exp.id}
                  fullWidth
                  multiline
                  sx={{
                    '& .MuiInputBase-root.Mui-disabled': {
                      backgroundColor: 'grey.100',
                    },
                  }}
                  className='col-span-4'
                  onChange={(e) => handleExperienceFieldChange(exp.id, "other", e.target.value)}
                />
              </Box>
              {editExperienceMode?.experienceId === exp.id && (
                <Box display="flex" justifyContent="flex-end" flexGrow={1} mt={4}>
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
              )}    
            </Paper>
          ))}
        </Box>
    )
}