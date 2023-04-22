import {Grid} from "@mui/material";
import {SearchForm} from "../components/SearchForm";
import {Navbar} from "../components/navbar/Navbar";

const styles = {
    root: {
        background: '#E4FDE1',
        height: '100vh',
    }
};

export default function HomePage() {

    return (
        <Grid sx={styles.root}>
            <Navbar/>
            <SearchForm/>
        </Grid>
    );
}