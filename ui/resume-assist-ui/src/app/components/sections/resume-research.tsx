'use client';
import { useState } from 'react';
import { TextField, Typography, Box, Paper, FormGroup,FormControlLabel, IconButton, Button, Divider, Checkbox } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import AddIcon from '@mui/icons-material/Add';
import { Add, Edit, Delete } from '@mui/icons-material';
import { green, blue, purple } from "@mui/material/colors"

export default function Researches({ onResumeChange, resume }) {
    const [experiences, setExperiences] = useState([]);
    const [editExperienceMode, setEditExperienceMode] = useState<{ experienceId: number | null } | null>(null);
  
    const handleAddExperience = () => {
      const newId = experiences.length + 1;
      setExperiences([...experiences, { id: newId, title: '', authors: '', conference: '' }]);
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
          researches: experiences,
      });
    }
    

    return (
        <Box className="mb-6">
          <Divider sx={{ borderBottomWidth: '2px'}}/>
          <Box display="flex" className="gap-2 mt-1" alignItems="center" mb={1}>
            <Typography variant="h6" className="pb-2 pt-4" flexGrow={1}>Publications</Typography>
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
                Add your first publication
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
              <Box>
                <Box className="grid grid-cols-4 gap-4 mb-0">
                    <Typography variant="subtitle1" className='col-span-2'>Title</Typography>
                </Box>
                <Box className="grid grid-cols-4 gap-4 mb-4">
                    <TextField
                    variant="outlined"
                    size="small"
                    value={exp.title}
                    disabled={editExperienceMode?.experienceId !== exp.id}
                    fullWidth
                    multiline
                    sx={{
                        '& .MuiInputBase-root.Mui-disabled': {
                        backgroundColor: 'grey.100',
                        },
                    }}
                    className='col-span-4'
                    onChange={(e) => handleExperienceFieldChange(exp.id, "title", e.target.value)}
                    />
                </Box>
              </Box>
              <Box>
                <Box className="grid grid-cols-4 gap-4 mb-0">
                    <Typography variant="subtitle1" className='col-span-2'>Authors</Typography>
                </Box>
                <Box className="grid grid-cols-4 gap-4 mb-4">
                    <TextField
                    variant="outlined"
                    size="small"
                    value={exp.authors}
                    disabled={editExperienceMode?.experienceId !== exp.id}
                    fullWidth
                    multiline
                    sx={{
                        '& .MuiInputBase-root.Mui-disabled': {
                        backgroundColor: 'grey.100',
                        },
                    }}
                    className='col-span-4'
                    onChange={(e) => handleExperienceFieldChange(exp.id, "authors", e.target.value)}
                    />
                </Box>
              </Box>
              <Box>
                <Box className="grid grid-cols-4 gap-4 mb-0">
                    <Typography variant="subtitle1" className='col-span-2'>Conference</Typography>
                </Box>
                <Box className="grid grid-cols-4 gap-4 mb-4">
                    <TextField
                    variant="outlined"
                    size="small"
                    value={exp.conference}
                    disabled={editExperienceMode?.experienceId !== exp.id}
                    fullWidth
                    multiline
                    sx={{
                        '& .MuiInputBase-root.Mui-disabled': {
                        backgroundColor: 'grey.100',
                        },
                    }}
                    className='col-span-4'
                    onChange={(e) => handleExperienceFieldChange(exp.id, "conference", e.target.value)}
                    />
                </Box>
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