import {AppBar, Box} from "@mui/material";
import {ROUTES} from "../../routes/routes";
import {Link} from "react-router-dom";

const styles = {
    logo: {
        width: '170px',
        height: '35px',
        p: 2,
        //border: '3px solid grey',
        position: 'relative',
        left: '20px',
        textAlign: 'center',
    },
    link: {
        color: 'white',
        textDecoration: 'none',
        fontFamily: 'Verdana',
        fontSize: '30px',
    }
};

export function Navbar() {
    return (
        <AppBar position="static"
            sx={{
                height: '12vh',
                background: '#F45B69',
                justifyContent: 'center',
            }}>
            <Box component="span" sx={styles.logo}>
                <Link to={ROUTES.HOME}
                    style={styles.link}>
                    Flat Finder
                </Link>
            </Box>
        </AppBar>
    );
}