import React, { useState } from 'react';
import { Box, Button, TextField, Typography, IconButton, Divider, Paper } from '@mui/material';
import { Add, Edit, Delete } from '@mui/icons-material';
import { green, blue, purple } from "@mui/material/colors"
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

interface Skill {
  catName: string;
  name: string;
}

interface Category {
  name: string;
  skills: Skill[];
}

export default function Skills({ onResumeChange, resume, job }) {
    const [categories, setCategories] = useState<Category[]>([]);
    const [editCategoryMode, setEditCategoryMode] = useState<{ categoryId: string | null } | null>(null);
    const [editSkillMode, setEditSkillMode] = useState<{ catName: string | null, skillName: string | null } | null>(null);
    const [newCategoryName, setNewCategoryName] = useState<string | null>(null);
    const [newSkillName, setNewSkillName] = useState<string | null>(null);


    const handleAddCategory = () => {
        setCategories([...categories, { name: `New Category ${categories.length + 1}`, skills: [] }]);
    };

    const handleDeleteCategory = (catName: string) => {
        setCategories(categories.filter(cat => cat.name !== catName));
    };

    const handleEditCategoryName = (catName: string, newName: string) => {
        setCategories(categories.map(cat => cat.name === catName ? { ...cat, name: newName } : cat));
        setEditCategoryMode(null);
        setNewCategoryName(null);
    };

    const handleAddSkill = (catName: string, skillName: string) => {
        const newSkill = { name: skillName, catName: catName };
        setCategories(categories.map(cat => cat.name === catName ? { ...cat, skills: [...cat.skills, newSkill] } : cat));
    };

    const handleDeleteSkill = (catName: string, skillName: string) => {
        setCategories(categories.map(cat => cat.name === catName ? { ...cat, skills: cat.skills.filter(skill => skill.name !== skillName) } : cat));
    };

    const handleEditSkillName = (catName: string, oldName: string, newName: string) => {
        console.log(catName, oldName, newName)
        setCategories(categories.map(cat => cat.name === catName ? {
            ...cat,
            skills: cat.skills.map(skill => skill.name === oldName ? { ...skill, name: newName } : skill)
        } : cat));
        setEditSkillMode(null);
        setNewSkillName(null);
    };

    const handleAssist = async () => {
        console.log(resume, job, categories);
        try {
            // Send a POST request to your backend
            const response = await fetch('/skills/assist', {
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
          skills: categories,
      });
    }

    const handleDragEnd = (result: any) => {
      if (!result.destination) return;

      const { source, destination } = result;
      const { droppableId: categoryId, index: srcIndex } = source;
      const { index: destIndex } = destination;

      const updatedCategories = [...categories];
      const category = updatedCategories.find(cat => cat.name === categoryId);

      if (category) {
          const [movedSkill] = category.skills.splice(srcIndex, 1);
          category.skills.splice(destIndex, 0, movedSkill);
          setCategories(updatedCategories);
      }
    };
    
    return (
      <>
      <Divider sx={{ borderBottomWidth: '2px'}}/>
      <DragDropContext onDragEnd={handleDragEnd} >
        <Box className="mb-2 mt-4">
          <Box display="flex" className="gap-2" alignItems="center" mb={2}>
            <Typography variant="h6" flexGrow={1}>
              Skills
            </Typography>
            <Button
              variant="contained"
              size="small"
              sx={{ 
                backgroundColor: purple[300],
                '&:hover': {
                  backgroundColor: purple[500], // Change color on hover
                },
              }}
              onClick={handleAddCategory}
              startIcon={<Add />}
              >
              Add Category
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
          {categories.length === 0 && (
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
                Add your first skill category
              </Typography>
            </Paper>
          )}
          {categories.map(category => (
            <Box key={category.name} mb={2}>
              {editCategoryMode?.categoryId === category.name && (
                <Box mb={2} p={2} sx={{ border: '1px solid #ccc', borderRadius: '4px' }}>
                  <Box display="flex" className="gap-2" alignItems="center">
                    <TextField
                        variant='standard'
                        value={newCategoryName ?? category.name}
                        onChange={(e) => setNewCategoryName(e.target.value)}
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
                      onClick={() => newCategoryName && handleEditCategoryName(category.name, newCategoryName)}
                      >
                      Save
                    </Button>
                    <Button
                      variant="contained"
                      color="secondary"
                      size="small"
                      onClick={() => {
                        setEditCategoryMode(null);
                        setNewCategoryName(null);
                      }}
                      >
                      Cancel
                    </Button>
                  </Box>
                </Box>
              )}
              {editSkillMode?.catName == category.name && (
                <Box mb={2} p={2} sx={{ border: '1px solid #ccc', borderRadius: '4px' }}>
                  <Box display="flex" className="gap-2" alignItems="center">
                    <TextField
                        variant='standard'
                        value={newSkillName ?? editSkillMode.skillName}
                        onChange={(e) => setNewSkillName(e.target.value)}
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
                      onClick={() => newSkillName && handleEditSkillName(category.name, editSkillMode.skillName, newSkillName)}
                      >
                      Save
                    </Button>
                    <Button
                      variant="contained"
                      color="secondary"
                      size="small"
                      onClick={() => {
                        setEditSkillMode(null);
                        setNewSkillName(null);
                      }}
                      >
                      Cancel
                    </Button>
                  </Box>
                </Box>
              )}
              <Paper elevation={2} sx={{ p: 2 }}>
                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <Typography variant="subtitle1">{category.name}</Typography>
                  <Box>
                    <Button
                      variant="outlined"
                      color="primary"
                      size="small"
                      onClick={() => handleAddSkill(category.name, `New Skill ${category.skills.length + 1}`)}
                      startIcon={<Add />}
                      >
                      Add Skill
                    </Button>
                    <IconButton
                      size="small"
                      aria-controls="category-menu"
                      aria-haspopup="true"
                      onClick={() => setEditCategoryMode({ categoryId: category.name })}
                    >
                      <Edit />
                    </IconButton>
                    <IconButton size="small" onClick={() => handleDeleteCategory(category.name)}>
                      <Delete />
                    </IconButton>
                  </Box>
                </Box>
                  <Droppable droppableId={category.name} direction="horizontal">
                    {(provided) => (
                      <Box
                      ref={provided.innerRef}
                      {...provided.droppableProps}
                      mt={2}
                      sx={{ display: 'flex', flexWrap: 'wrap' }}
                      >
                      {category.skills.map((skill, index) => (
                        <Draggable key={skill.catName} draggableId={skill.catName} index={index}>
                          {(provided) => (
                            <Paper
                                ref={provided.innerRef}
                                {...provided.draggableProps}
                                {...provided.dragHandleProps}
                                sx={{
                                  display: 'flex',
                                  p: 1,
                                  m: 1,
                                  
                                }}
                                className="skill-cell"
                                >
                              <Typography variant="body2" className="pr-1">
                                {skill.name}
                              </Typography>
                              
                              <IconButton
                                sx = {{
                                  width: "13px",
                                  height: "18px",
                                  '& .MuiSvgIcon-root': {
                                    fontSize: '12px', // Adjust the size of the icon
                                  },
                                }}
                                onClick={() => {
                                  setEditSkillMode({ catName: category.name, skillName: skill.name });
                                }}
                                >
                                <Edit />
                              </IconButton>
                              <IconButton
                                sx = {{
                                  width: "13px",
                                  height: "18px",
                                  '& .MuiSvgIcon-root': {
                                    fontSize: '12px', // Adjust the size of the icon
                                  },
                                }}
                                onClick={() => handleDeleteSkill(category.name, skill.name)}
                                >
                                <Delete />
                              </IconButton>
                            </Paper>
                          )}
                        </Draggable>
                      ))}
                    {provided.placeholder}
                  </Box>
                )}
              </Droppable>
            </Paper>
          </Box>
        ))}
      </Box>
    </DragDropContext>
    </>
  );
}