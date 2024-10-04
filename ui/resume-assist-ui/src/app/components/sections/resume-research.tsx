'use client';
import { useState } from 'react';
import { TextField, Typography, Box, Paper, IconButton, Button, Divider } from '@mui/material';
import dayjs from 'dayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { MobileDatePicker } from '@mui/x-date-pickers/MobileDatePicker';
import AddIcon from '@mui/icons-material/Add';
import { Edit, Delete } from '@mui/icons-material';
import { green, purple } from "@mui/material/colors"
import { v4 as uuidv4 } from 'uuid';

export default function Researches({ onResumeChange, resume }) {
    const [researches, setResearchs] = useState([]);
    const [editResearchMode, setEditResearchMode] = useState<{ researchId: number | null } | null>(null);
  
    const handleAddResearch = () => {
      const newId = researches.length + 1;
      const rId = uuidv4();
      setResearchs([...researches, { id: newId, rId: rId, title: '', authors: '', conference: '', date: null }]);
    };
  
    const handleRemoveResearch = (researchId) => {
      setResearchs(prevResearchs => {
        const filteredResearchs = prevResearchs.filter(exp => exp.id !== researchId);
        return filteredResearchs.map((exp, index) => ({
          ...exp,
          id: index + 1 // Numbering IDs based on their order in the list
        }));
      });
    };

    const handleResearchFieldChange = (researchId, field, value) => {
      setResearchs(researches.map(exp => exp.id === researchId ? {...exp, [field]: value} : exp));
    }
  
    const handleSaveAll = async () => {
      const researches_body = researches.map(exp => {
        const map = {
          research_id: exp.rId,
          title: exp.title,
          authors: exp.authors,
          conference: exp.conference,
          date: exp.date? dayjs(exp.date).format("MM/YYYY") : "",
        };
        return map;
      });
      // Call the API to save the education data
      try {
        // Send a POST request to your backend
        const response = await fetch(`/api/research/save`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(researches_body),
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
      } catch (error) {
          console.error('Failed to refresh PDF:', error);
      }

      onResumeChange({
          ...resume,
          researches: researches_body,
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
              onClick={handleAddResearch}
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
          {researches.length === 0 && (
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
          {researches.map(exp => (
            <Paper key={exp.id} elevation={2} className="p-4 mb-4">
              <Box display="flex" className="gap-2 mb-0" alignItems="center" mb={1}>
                  <Typography variant="h6" flexGrow={1}>#{exp.id}</Typography>
                  {editResearchMode?.researchId !== exp.id && (
                    <>
                      <IconButton
                        size="small"
                        aria-controls="category-menu"
                        aria-haspopup="true"
                        onClick={() => setEditResearchMode({ researchId: exp.id })}
                        >
                        <Edit />
                      </IconButton>
                      <IconButton size="small" onClick={() => handleRemoveResearch(exp.id)}>
                        <Delete />
                      </IconButton>
                    </>
                  )}
              </Box>
              <Box>
                <Box className="grid grid-cols-4 gap-4 mb-4">
                  <TextField
                    variant="outlined"
                    size="small"
                    label="Title"
                    value={exp.title}
                    disabled={editResearchMode?.researchId !== exp.id}
                    fullWidth
                    multiline
                    sx={{
                        '& .MuiInputBase-root.Mui-disabled': {
                        backgroundColor: 'grey.100',
                        },
                    }}
                    className='col-span-3'
                    onChange={(e) => handleResearchFieldChange(exp.id, "title", e.target.value)}
                  />
                  <LocalizationProvider dateAdapter={AdapterDayjs}>
                    <MobileDatePicker 
                      label="Date"
                      disableFuture={true}
                      value={exp.date}
                      disabled={editResearchMode?.researchId !== exp.id}
                      fullWidth
                      slotProps={{ textField: { size: 'small' } }}
                      sx={{
                        '& .MuiInputBase-root.Mui-disabled': {
                          backgroundColor: 'grey.100',
                        },
                      }}
                      className='col-span-1'
                      views={['month', 'year']}
                      onChange={(value) => handleResearchFieldChange(exp.id, "date", value)}
                    />
                  </LocalizationProvider>
                </Box>
              </Box>
              
              <Box>
                <Box className="grid grid-cols-4 gap-4 mb-4">
                    <TextField
                    variant="outlined"
                    size="small"
                    label="Conference"
                    value={exp.conference}
                    disabled={editResearchMode?.researchId !== exp.id}
                    fullWidth
                    multiline
                    sx={{
                        '& .MuiInputBase-root.Mui-disabled': {
                        backgroundColor: 'grey.100',
                        },
                    }}
                    className='col-span-4'
                    onChange={(e) => handleResearchFieldChange(exp.id, "conference", e.target.value)}
                    />
                </Box>
              </Box>
              <Box>
                <Box className="grid grid-cols-4 gap-4 mb-4">
                    <TextField
                    variant="outlined"
                    size="small"
                    label='Authors [split by ";" sign]'
                    value={exp.authors}
                    disabled={editResearchMode?.researchId !== exp.id}
                    fullWidth
                    multiline
                    sx={{
                        '& .MuiInputBase-root.Mui-disabled': {
                        backgroundColor: 'grey.100',
                        },
                    }}
                    className='col-span-4'
                    onChange={(e) => handleResearchFieldChange(exp.id, "authors", e.target.value)}
                    />
                </Box>
              </Box>
              {editResearchMode?.researchId === exp.id && (
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
                        onClick={() => setEditResearchMode(null)}
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