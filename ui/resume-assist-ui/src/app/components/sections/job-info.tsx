'use client';
import { TextField, Typography, Box, Paper } from '@mui/material';

export default function JobInfo({ onJobChange, job }) {
    const handleChange = (field) => (event) => {
        const { value } = event.target;
        onJobChange({
            ...job,
            [field]: value,
        });
    };

    return (
        <Paper elevation={3} className="w-full p-10 mt-0 mb-6">
            <Typography variant="h5" className="mb-12 pb-4">
                <b>Job Details</b>
            </Typography>
            <Box component="form" className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex flex-col space-y-4">
                    <TextField
                        label="Job Position"
                        variant="outlined"
                        size="small"
                        fullWidth
                        value={job.position}
                        onChange={handleChange('position')}
                    />
                    <TextField
                        label="Company Name"
                        variant="outlined"
                        size="small"
                        fullWidth
                        value={job.company}
                        onChange={handleChange('company')}
                    />
                    <TextField
                        label="Job Link"
                        variant="outlined"
                        size="small"
                        fullWidth
                        value={job.url}
                        onChange={handleChange('url')}
                    />
                </div>
                <TextField
                    label="Job Description"
                    variant="outlined"
                    size="small"
                    multiline
                    rows={6}
                    fullWidth
                    value={job.description}
                    onChange={handleChange('description')}
                />
            </Box>
        </Paper>
    );
}