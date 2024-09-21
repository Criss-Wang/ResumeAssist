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
import { Hind_Guntur } from 'next/font/google';

export default function Projects({ onResumeChange, resume, job }) {
    const [projects, setProjects] = useState([]);
    const [editProjectMode, setEditProjectMode] = useState<{ projectId: number | null } | null>(null);
    const [newHighlight, setNewHighlight] = useState<{ id: number, hid: number, value: string } | null>(null);
  
    const handleAddProject = () => {
      const newId = projects.length + 1;
      setProjects([...projects, { id: newId, projectName: '', startDate: null, endDate: null, url: '', current: false, highlights: [] }]);
    };
  
    const handleRemoveProject = (projectId) => {
      setProjects(prevProjects => {
        const filteredProjects = prevProjects.filter(exp => exp.id !== projectId);
        return filteredProjects.map((exp, index) => ({
          ...exp,
          id: index + 1 // Numbering IDs based on their order in the list
        }));
      });
    };

    const handleProjectFieldChange = (projectId, field, value) => {
      setProjects(projects.map(exp => exp.id === projectId ? {...exp, [field]: value} : exp));
    }
  
    const handleAddHighlight = (project) => {
      const id = project.highlights.length + 1;
      setProjects(projects.map(exp => exp.id === project.id ? { ...exp, highlights: [...exp.highlights, { id: id, value: "new highlight" }] } : exp));
    };
  
    const handleRemoveHighlight = (projectId, hId) => {
      setProjects(projects.map(exp => exp.id === projectId ? { ...exp, highlights: exp.highlights.filter(h => h.id !== hId) } : exp));
    };
  
    const handleHighlightChange = () => {
      setProjects(projects.map(exp => exp.id === newHighlight.id ? { 
        ...exp, 
        highlights: exp.highlights.map(h => h.id === newHighlight.hid ? { ...h, value: newHighlight.value } : h) 
      } : exp));
      setNewHighlight(null);
    };


    const handleAssist = async (project) => {
      try {
          // Send a POST request to your backend
          console.log(project);
          const response = await fetch('/api/project/assist', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({ resume: resume, project: project }),
          });
          const results = await response.json();
          const updatedHighlights = results.map((r, idx) => { 
            const highlight = {
              id: project.id, hid: idx, value: r
            }; 
            return highlight; 
          });
          handleProjectFieldChange(project.id, "highlights", updatedHighlights);
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
      } catch (error) {
          console.error('Failed to refresh PDF:', error);
      }
    };
  
    const handleSaveAll = async () => {
      const projectPayload = projects.map(exp => {
        const map = {
          id: exp.id,
          project_name: exp.projectName,
          start_date: dayjs(exp.startDate).format("MM/YYYY"),
          end_date: exp.endDate? dayjs(exp.endDate).format("MM/YYYY") : "",
          url: exp.url,
          current: exp.current,
          highlights: exp.highlights.map(h => h.value),
        };
        return map;
      });
      try {
        // Send a POST request to your backend
        const response = await fetch(`/api/project/save/${resume.id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(projectPayload),
        });
  
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
      } catch (error) {
          console.error('Failed to refresh PDF:', error);
      }
      onResumeChange({
          ...resume,
          projects: projects,
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
              onClick={handleAddProject}
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
          {projects.length === 0 && (
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
          {projects.map(exp => (
            <Paper key={exp.id} elevation={2} className="p-4 mb-4">
                <Box display="flex" className="gap-2 mb-0" alignItems="center" mb={1}>
                  <Typography variant="h6" flexGrow={1}>#{exp.id}</Typography>
                  {editProjectMode?.projectId !== exp.id && (
                    <>
                      <IconButton
                        size="small"
                        aria-controls="category-menu"
                        aria-haspopup="true"
                        onClick={() => setEditProjectMode({ projectId: exp.id })}
                        >
                        <Edit />
                      </IconButton>
                      <IconButton size="small" onClick={() => handleRemoveProject(exp.id)}>
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
                  disabled={editProjectMode?.projectId !== exp.id}
                  fullWidth
                  sx={{
                    '& .MuiInputBase-root.Mui-disabled': {
                      backgroundColor: 'grey.100',
                    },
                  }}
                  className='col-span-4'
                  onChange={(e) => handleProjectFieldChange(exp.id, "projectName", e.target.value)}
                />
              </Box>
              <Box className="grid grid-cols-12 gap-4 mb-2">
                <TextField
                  variant="outlined"
                  size="small"
                  label="Codebase Link"
                  value={exp.url}
                  disabled={editProjectMode?.projectId !== exp.id}
                  fullWidth
                  sx={{
                    '& .MuiInputBase-root.Mui-disabled': {
                      backgroundColor: 'grey.100',
                    },
                  }}
                  className='col-span-6'
                  onChange={(e) => handleProjectFieldChange(exp.id, "url", e.target.value)}
                />
                <LocalizationProvider dateAdapter={AdapterDayjs}>
                  <MobileDatePicker 
                    label="Start Date"
                    disableFuture={true}
                    value={exp.startDate}
                    disabled={editProjectMode?.projectId !== exp.id}
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
                    onChange={(value) => handleProjectFieldChange(exp.id, "startDate", value)}
                  />
                </LocalizationProvider>
                <LocalizationProvider dateAdapter={AdapterDayjs}>
                  <MobileDatePicker 
                    label="End Date"
                    disableFuture={true}
                    value={exp.current ? null : exp.endDate}
                    disabled={editProjectMode?.projectId !== exp.id || exp.current}
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
                    onChange={(value) => handleProjectFieldChange(exp.id, "endDate", value)}
                  />
                </LocalizationProvider>
                <FormGroup>
                  <FormControlLabel 
                    control={<Checkbox 
                      disabled={editProjectMode?.projectId !== exp.id}
                      checked={exp.current}
                      onChange={(e) => handleProjectFieldChange(exp.id, "current", e.target.checked)}
                    />} 
                    label={<span className="text-black">Current</span>}
                    labelPlacement="end"
                    sx={{fontcolor: "black"}}
                    className='pl-1'
                  />
                </FormGroup>
              </Box>
              <Typography variant="subtitle1" className='pl-1 mb-2 pb-2 underline italic'>Highlights</Typography>
              {exp.highlights.map((h, idx) => (
                <>
                  {newHighlight?.id === exp.id && newHighlight?.hid === h.id && (
                    <Box key={idx} mb={2} p={1} sx={{ border: '1px solid #ccc', borderRadius: '4px' }}>
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
                    
                    {editProjectMode?.projectId === exp.id && (
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
                    {editProjectMode?.projectId == exp.id && (
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
              {editProjectMode?.projectId === exp.id && (
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
                      onClick={() => handleAssist(exp)}
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
                      onClick={() => setEditProjectMode(null)}
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