'use client';
import { useState } from 'react';
import AddIcon from '@mui/icons-material/Add';
import { TextField, Typography, Box, Paper, FormGroup,FormControlLabel, IconButton, Button, Divider, Checkbox } from '@mui/material';
import dayjs from 'dayjs';
import { MobileDatePicker } from '@mui/x-date-pickers/MobileDatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { Edit, Delete } from '@mui/icons-material';
import { green, purple } from "@mui/material/colors"


export default function Education({ onResumeChange, resume }) {
    const [educations, setEducations] = useState([]);
    const [editEducationMode, setEditEducationMode] = useState<{ educationId: number | null } | null>(null);
  
    const handleAddEducation = () => {
      const newId = educations.length + 1;
      setEducations([...educations, { id: newId, institution: '', area: '', degree: '', startDate: null, endDate: null, current: false, courses: '', gpa: '', other: '' }]);
    };
  
    const handleRemoveEducation = (educationId) => {
      setEducations(prevEducations => {
        const filteredEducations = prevEducations.filter(exp => exp.id !== educationId);
        return filteredEducations.map((exp, index) => ({
          ...exp,
          id: index + 1 // Numbering IDs based on their order in the list
        }));
      });
    };

    const handleEducationFieldChange = (educationId, field, value) => {
      setEducations(educations.map(exp => exp.id === educationId ? {...exp, [field]: value} : exp));
    }
  
    const handleSaveAll = async () => {
      const requestContent = educations.map(exp => {
        const map = {
          institution: exp.institution,
          area: exp.area,
          degree: exp.degree,
          current: exp.current,
          gpa: exp.gpa,
          courses: exp.courses,
          other: exp.other,
          start_date: dayjs(exp.startDate).format("MM/YYYY"),
          end_date: exp.endDate? dayjs(exp.endDate).format("MM/YYYY") : "",
        };
        return map;
      });
      console.log(requestContent);
      // Call the API to save the education data
      try {
        // Send a POST request to your backend
        const response = await fetch(`/api/education/save/${resume.id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestContent),
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
      } catch (error) {
          console.error('Failed to refresh PDF:', error);
      }

      onResumeChange({
          ...resume,
          educations: educations,
      })
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
              onClick={handleAddEducation}
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
          {educations.length === 0 && (
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
          {educations.map(exp => (
            <Paper key={exp.id} elevation={2} className="p-4 mb-4">
                <Box display="flex" className="gap-2 mb-0" alignItems="center" mb={1}>
                  <Typography variant="h6" flexGrow={1}>#{exp.id}</Typography>
                  {editEducationMode?.educationId !== exp.id && (
                    <>
                      <IconButton
                        size="small"
                        aria-controls="category-menu"
                        aria-haspopup="true"
                        onClick={() => setEditEducationMode({ educationId: exp.id })}
                        >
                        <Edit />
                      </IconButton>
                      <IconButton size="small" onClick={() => handleRemoveEducation(exp.id)}>
                        <Delete />
                      </IconButton>
                    </>
                  )}
              </Box>
              <Box className="grid grid-cols-4 gap-4 mb-4">
                <TextField
                  variant="outlined"
                  size="small"
                  label="Institution"
                  value={exp.institution}
                  disabled={editEducationMode?.educationId !== exp.id}
                  fullWidth
                  sx={{
                    '& .MuiInputBase-root.Mui-disabled': {
                      backgroundColor: 'grey.100',
                    },
                  }}
                  className='col-span-3'
                  onChange={(e) => handleEducationFieldChange(exp.id, "institution", e.target.value)}
                />
                <TextField
                  variant="outlined"
                  size="small"
                  label="Degree"
                  value={exp.degree}
                  disabled={editEducationMode?.educationId !== exp.id}
                  fullWidth
                  sx={{
                    '& .MuiInputBase-root.Mui-disabled': {
                      backgroundColor: 'grey.100',
                    },
                  }}
                  className='col-span-1'
                  onChange={(e) => handleEducationFieldChange(exp.id, "degree", e.target.value)}
                />
              </Box>
              <Box className="grid grid-cols-10 gap-4 mb-2">
                <Box className="col-span-9 gap-4 mb-0">
                  <Box className="grid grid-cols-9 gap-4 mb-2">
                    <TextField
                      variant="outlined"
                      size="small"
                      label="Major"
                      value={exp.area}
                      disabled={editEducationMode?.educationId !== exp.id}
                      fullWidth
                      sx={{
                        '& .MuiInputBase-root.Mui-disabled': {
                          backgroundColor: 'grey.100',
                        },
                      }}
                      className='col-span-4'
                      onChange={(e) => handleEducationFieldChange(exp.id, "area", e.target.value)}
                    />
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                      <MobileDatePicker 
                        label="Start Date"
                        disableFuture={true}
                        value={exp.startDate}
                        disabled={editEducationMode?.educationId !== exp.id}
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
                        onChange={(value) => handleEducationFieldChange(exp.id, "startDate", value)}
                      />
                    </LocalizationProvider>
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                      <MobileDatePicker 
                        label="End Date"
                        disableFuture={true}
                        value={exp.current ? null : exp.endDate}
                        disabled={editEducationMode?.educationId !== exp.id || exp.current}
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
                        onChange={(value) => handleEducationFieldChange(exp.id, "endDate", value)}
                      />
                    </LocalizationProvider>
                    <FormGroup>
                      <FormControlLabel 
                        control={<Checkbox 
                          disabled={editEducationMode?.educationId !== exp.id}
                          checked={exp.current}
                          onChange={(e) => handleEducationFieldChange(exp.id, "current", e.target.checked)}
                        />} 
                        label={<span className="text-black">Current</span>}
                        labelPlacement="end"
                        sx={{fontcolor: "black"}}
                        className='pl-6'
                      />
                    </FormGroup>
                  </Box>
                </Box>
              </Box>
              <Box className="grid grid-cols-8 gap-4 mb-4">
                <TextField
                  variant="outlined"
                  size="small"
                  label="GPA"
                  value={exp.gpa}
                  disabled={editEducationMode?.educationId !== exp.id}
                  fullWidth
                  sx={{
                    '& .MuiInputBase-root.Mui-disabled': {
                      backgroundColor: 'grey.100',
                    },
                  }}
                  className='col-span-1'
                  onChange={(e) => handleEducationFieldChange(exp.id, "gpa", e.target.value)}
                />
                <TextField
                  variant="outlined"
                  size="small"
                  label="Courseworks"
                  value={exp.courses}
                  disabled={editEducationMode?.educationId !== exp.id}
                  fullWidth
                  sx={{
                    '& .MuiInputBase-root.Mui-disabled': {
                      backgroundColor: 'grey.100',
                    },
                  }}
                  className='col-span-7'
                  onChange={(e) => handleEducationFieldChange(exp.id, "courses", e.target.value)}
                />
              </Box>
              <Box className="grid grid-cols-4 gap-4 mb-4">
                <TextField
                  variant="outlined"
                  size="small"
                  label='Highlights [split by ";" sign]'
                  value={exp.other}
                  disabled={editEducationMode?.educationId !== exp.id}
                  fullWidth
                  multiline
                  sx={{
                    '& .MuiInputBase-root.Mui-disabled': {
                      backgroundColor: 'grey.100',
                    },
                  }}
                  className='col-span-4'
                  onChange={(e) => handleEducationFieldChange(exp.id, "other", e.target.value)}
                />
              </Box>
              {editEducationMode?.educationId === exp.id && (
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
                        onClick={() => setEditEducationMode(null)}
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