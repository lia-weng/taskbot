import React from "react"
import { useEffect, useState } from "react"
import Cookies from "js-cookie"
import { useNavigate } from "react-router-dom"
import img from "../images/Web-developer.svg"
import { Link } from "react-router-dom"

const baseURL = "https://oyster-ace-sturgeon.ngrok-free.app"

const LoginButton = () => {
  const handleLogin = () => {
    window.location.href = `${baseURL}/authorize`
  }

  return (
    <button
      className="text-white bg-sky-800 hover:bg-sky-700 inline-flex items-center justify-center w-full px-6 py-2 my-4 text-lg shadow-xl rounded-2xl sm:w-auto sm:mb-0 group"
      onClick={handleLogin}
    >
      Log In
    </button>
  )
}

const Intro = () => {
  const [loggedIn, setLoggedIn] = useState(false)
  //   const navigate = useNavigate()

  useEffect(() => {
    const authCookie = Cookies.get("authenticated")

    if (authCookie === "true") {
      setLoggedIn(true)
    }
  }, [])

  return (
    <>
      <div>{loggedIn && <p>You're logged in!</p>}</div>
      <div
        className="flex flex-col py-16 lg:py-20 px-14 items-center"
        id="about"
        data-aos="fade-up"
        data-aos-delay="500"
      >
        <h2 className="mb-5 text-center text-3xl text-sky-800 font-bold underline underline-offset-8">
          Get Started
        </h2>

        <div className="flex flex-col lg:flex-row text-center lg:text-left mt-10 w-full lg:max-w-4xl">
          <h3 className="text-3xl text-sky-800 font-bold my-2 lg:w-1/4">
            Step 1:
          </h3>
          <div className="my-2 lg:w-3/4">
            <p className="text-xl text-gray-600 font-semibold">
              Sign in to your Google account.
            </p>
            {/* <Link to="/contact" className="text-white bg-sky-800 hover:bg-sky-700 inline-flex items-center justify-center w-full px-6 py-2 my-4 text-lg shadow-xl rounded-2xl sm:w-auto sm:mb-0 group">
                            Sign in
                            <svg className="w-4 h-4 ml-1 group-hover: translate-x-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd"></path></svg>
                        </Link> */}
            <LoginButton />
          </div>
        </div>
        <div className="flex flex-col lg:flex-row text-center lg:text-left mt-10 w-full max-w-4xl">
          <h3 className="text-3xl text-sky-800 font-bold my-2 lg:w-1/4">
            Step 2:
          </h3>
          <div className="my-2 lg:w-3/4">
            <p className="text-xl text-gray-600 font-semibold">
              Add some tasks to the "taskbot" list.
            </p>
          </div>
        </div>
        <div className="flex flex-col lg:flex-row text-center lg:text-left mt-10 w-full max-w-4xl">
          <h3 className="text-3xl text-sky-800 font-bold my-2 lg:w-1/4">
            Step 3:
          </h3>
          <div className="my-2 lg:w-3/4">
            <p className="text-xl text-gray-600 font-semibold">
              Start using taskbot!
            </p>
          </div>
        </div>
      </div>
    </>
  )
}

export default Intro
