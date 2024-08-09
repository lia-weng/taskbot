import React from "react"
import { useEffect, useState } from "react"
import axios from "axios"
import Cookies from "js-cookie"
import "react-phone-number-input/style.css"
import PhoneInput, { isPossiblePhoneNumber } from "react-phone-number-input"
import Alert from "@mui/material/Alert"
import IconButton from "@mui/material/IconButton"
import EditIcon from "@mui/icons-material/Edit"
import Button from "@mui/material/Button"

import GetStartedDisplay from "./GetStartedDisplay"
import { GoogleLogin } from "../Button"
import taskListImg from "../../images/task-list.png"
import addTaskImg from "../../images/add-tasks.png"
import completeImg from "../../images/complete.svg"
import signInImg from "../../images/sign-in.svg"

const baseURL = "https://oyster-ace-sturgeon.ngrok-free.app"

const GetStarted = () => {
  const [loggedIn, setLoggedIn] = useState(false)
  const [phoneNumber, setPhoneNumber] = useState()
  const [phoneNumberError, setPhoneNumberError] = useState()
  const [phoneNumberComplete, setPhoneNumberComplete] = useState(false)

  useEffect(() => {
    const authCookie = Cookies.get("authenticated")

    if (authCookie === "true") {
      setLoggedIn(true)
    } else {
      setLoggedIn(false)
    }
  }, [loggedIn])

  const handleSubmit = async (e) => {
    e.preventDefault()

    console.log("number", phoneNumber)
    if (!phoneNumber || !isPossiblePhoneNumber(phoneNumber)) {
      setPhoneNumberError("Please enter a valid phone number.")
    } else {
      setPhoneNumberError()
      setPhoneNumberComplete(true)

      try {
        await axios.post("/api/submit-phone", { phoneNumber })
      } catch (error) {
        console.error("Error submitting phone number:", error)
        setPhoneNumberError(
          "Sorry, something went wrong. Please try another number."
        )
      }
    }
  }

  const steps = [
    {
      content: loggedIn ? (
        <p className="big-text">Connected to: {Cookies.get("email")}</p>
      ) : (
        <>
          <p className="big-text mb-8">
            Taskbot uses Google Tasks. Click below to connect your account.
          </p>
          <GoogleLogin
            onClick={() => (window.open = `${baseURL}/authorize`)}
            label={"Connect to Google"}
          />
          <div className="w-full h-full pt-4 flex justify-center overflow-hidden">
            <img alt="sign in img" className="scale-75" src={signInImg} />
          </div>
        </>
      ),
    },
    {
      content: (
        <>
          <p className="big-text">
            Go to &nbsp;
            <a
              href={"https://tasks.google.com/"}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sky-600 underline"
            >
              Google Tasks
            </a>
            . You will see a new task list called "taskbot".
          </p>
          <div className="w-full h-full p-4 flex justify-center overflow-hidden">
            <img alt="task list img" src={taskListImg} />
          </div>
        </>
      ),
    },
    {
      content: (
        <>
          <p className="big-text">Add some tasks to "taskbot".</p>
          <div className="w-full h-full p-4 flex justify-center overflow-hidden">
            <img alt="add task img" src={addTaskImg} />
          </div>
        </>
      ),
    },
    {
      content: (
        <>
          {phoneNumberComplete ? (
            <>
              <p className="big-text">Awesome! Taskbot just texted you at:</p>
              <div className="flex items-center mt-8">
                <PhoneInput
                  international
                  defaultCountry="CA"
                  placeholder="Enter phone number"
                  value={phoneNumber}
                  onChange={setPhoneNumber}
                  className="text-xl text-gray-600 font-semibold"
                />
                <IconButton
                  color="primary"
                  aria-label="Edit phone number"
                  onClick={() => {
                    setPhoneNumberComplete(false)
                    setPhoneNumberError()
                  }}
                >
                  <EditIcon />
                </IconButton>
              </div>
            </>
          ) : (
            <>
              <p className="big-text">
                Taskbot will send you reminders through text.<br></br>Enter your
                phone number below.
              </p>
              <form
                onSubmit={handleSubmit}
                className="flex flex-col items-center mt-8"
              >
                <PhoneInput
                  international
                  defaultCountry="CA"
                  placeholder="Enter phone number"
                  value={phoneNumber}
                  onChange={setPhoneNumber}
                  className="big-text mb-8"
                />
                <Button variant="contained" color="primary" type="submit">
                  Confirm
                </Button>
              </form>
            </>
          )}
          {phoneNumberError ? (
            <Alert severity="error" className="mt-8">
              {phoneNumberError}
            </Alert>
          ) : (
            <></>
          )}
        </>
      ),
    },
    {
      content: (
        <>
          <p className="big-text">
            You're all set!<br></br>Taskbot will text you about upcoming tasks
            every day.
          </p>
          <div className="w-full h-full pt-4 flex justify-center overflow-hidden">
            <img alt="complete img" className="scale-75" src={completeImg} />
          </div>
        </>
      ),
    },
  ]

  return (
    <div
      className="flex flex-col py-16 lg:py-20 items-center text-center"
      id="get-started"
      data-aos="fade-up"
      data-aos-delay="500"
    >
      <h2 className="mb-5 text-center lg:text-4xl text-3xl text-sky-800 font-extrabold">
        Get Started
      </h2>
      <GetStartedDisplay steps={steps} />
    </div>
  )
}

export default GetStarted
