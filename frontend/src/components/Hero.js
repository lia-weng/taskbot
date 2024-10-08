import React from "react"
import { Link } from "react-router-dom"
import { HashLink } from "react-router-hash-link"
import Button from "@mui/material/Button"
import ArrowForwardIcon from "@mui/icons-material/ArrowForward"

import NavBar from "../components/Navbar/NavBar"
import heroImg from "../images/hero.svg"

const Hero = () => {
  return (
    <>
      <>
        <div className="hero w-full flex flex-col" id="hero">
          <div>
            <NavBar />
          </div>

          <div
            id="hero"
            className="flex flex-col lg:flex-row justify-between text-center lg:text-left mt-12 lg:mt-16 lg:p-12 xl:pl-20"
            // data-aos="zoom-in"
          >
            <div
              className="lg:w-1/2 flex flex-col justify-center px-5 pt-12 lg:pt-0 lg:pl-12 xl:"
              // data-aos="zoom-in"
              // data-aos-delay="200"
            >
              <h1 className="mb-5 lg:text-5xl text-3xl font-extrabold text-sky-800">
                Taskbot
              </h1>
              <div className="tracking-tight mb-12 big-text">
                The personal AI assistant to help you get things done.
              </div>
              <HashLink smooth to="/#get-started">
                <Button
                  variant="contained"
                  color="primary"
                  endIcon={<ArrowForwardIcon />}
                  size="large"
                >
                  Get Started
                </Button>
              </HashLink>
            </div>
            <div
              className="flex justify-center w-full lg:w-1/2"
              // data-aos="fade-up"
              // data-aos-delay="700"
            >
              <img
                alt="hero img"
                className="rounded-t float-right duration-1000 w-4/5 mt-10 lg:mt-0"
                src={heroImg}
              />
              {/* <img
                alt="card img"
                className="rounded-t float-right duration-1000 w-full mt-10 lg:mt-0"
                src={heroImg}
              /> */}
            </div>
          </div>
        </div>
      </>
    </>
  )
}

export default Hero
