// create defualt react compnent template for a next ui navbar
import React from 'react';
import { Navbar, Nav, NavItem, NavLink } from 'reactstrap';

const CustomNavbar = () => {
    return (
        <Navbar color="light" light expand="md">
            <Nav className="mr-auto" navbar>
                <NavItem>
                    <NavLink href="/">Home</NavLink>
                </NavItem>
                <NavItem>
                    <NavLink href="/about">About</NavLink>
                </NavItem>
                <NavItem>
                    <NavLink href="/contact">Contact</NavLink>
                </NavItem>
            </Nav>
        </Navbar>
    );
};

export default CustomNavbar;