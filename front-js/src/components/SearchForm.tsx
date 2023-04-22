import {Button, Grid, TextField, Typography} from "@mui/material";
import {useState} from "react";

const styles = {
    root: {
        justifyContent: 'center',
        alignItems: 'center',
        position: 'relative',
        height: '70vh',
    },
    text: {
        margin: '60px',
        textAlign: 'center',
        color: '#456990',
    },
    textField: {
        width: '50%',
    },
    searchButton: {
        position: 'relative',
        left: '20%',
        top: '20px',
        backgroundColor: '#456990',
        '&:hover': {
            backgroundColor: '#114B5F',
        }
    }
};


export function SearchForm() {

    const [value, setValue] = useState<string>('');
    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setValue(event.target.value);
    };


    return (
        <Grid container
            direction="column"
            sx={styles.root}>
            <Typography
                sx={styles.text}
                variant="h3">Where should we look for?</Typography>
            <TextField
                sx={styles.textField}
                id="margin-none"
                label="Provide link"
                type="search"
                value={value}
                onChange={handleChange}/>
            <Button
                variant="contained"
                sx={styles.searchButton}
                disabled={value.length == 0}>
                Search
            </Button>
        </Grid>
    );
}