import React from "react"
import { Link } from "react-router-dom"
import NavBar from "../components/Navbar/NavBar"
import heroImg from "../images/web-dev.svg"

const Hero = () => {
  return (
    <>
      <div className="hero" id="hero">
        <div>
          <NavBar />
        </div>
        <div
          id="hero"
          className="flex flex-col p-10 mt-20 lg:p-20 justify-between text-center bg-gray-100"
        >
          {/* <div className="flex flex-col justify-center" > */}
          <h1 className="mb-5 md:text-5xl text-3xl font-bold text-sky-800">
            taskbot
          </h1>
          <div className="text-xl font-semibold tracking-tight mb-5 text-gray-500">
            The personal AI assistant to help you get things done.
          </div>
        </div>
      </div>
    </>
  )
}

export default Hero
