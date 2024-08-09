import React from "react"
import { useEffect, useState } from "react"
import axios from "axios"
import Cookies from "js-cookie"
import "react-phone-number-input/style.css"
import PhoneInput, {
  formatPhoneNumber,
  formatPhoneNumberIntl,
  isPossiblePhoneNumber,
  isValidPhoneNumber,
} from "react-phone-number-input"
import Alert from "@mui/material/Alert"
import IconButton from "@mui/material/IconButton"
import EditIcon from "@mui/icons-material/Edit"
import Carousel from "react-material-ui-carousel"
import Button from "@mui/material/Button"

import { GoogleLogin } from "./Button"
import GetStartedStep from "./GetStartedStep"
import taskListImg from "../images/task-list.png"
import addTaskImg from "../images/add-tasks.png"

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
            Taskbot uses Google Tasks.<br></br>Click below to connect your
            Google account.
          </p>
          <GoogleLogin
            onClick={() => (window.open = `${baseURL}/authorize`)}
            label={"Connect to Google"}
          />
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
          <img
            src={taskListImg}
            alt="Task list called 'taskbot'"
            className="mt-5"
          />
        </>
      ),
    },
    {
      content: (
        <>
          <p className="big-text">Add some tasks to "taskbot".</p>
          <img
            src={addTaskImg}
            alt="Add some tasks to 'taskbot'"
            className="mt-5"
          />
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
                Taskbot will send you reminders through text. 💬<br></br>Enter
                your phone number below.
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
                  className="text-xl text-gray-600 font-semibold mb-8"
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
            You're all set!<br></br>Keep an eye out on for texts from Taskbot 👀
          </p>
        </>
      ),
    },
  ]

  return (
    <>
      <div
        className="flex flex-col py-16 lg:py-20 items-center text-center"
        id="get-started"
        data-aos="fade-up"
        data-aos-delay="500"
      >
        <h2 className="mb-5 text-center text-2xl md:text-3xl text-sky-800 font-extrabold underline underline-offset-8">
          Get Started
        </h2>

        {/* Display the steps on smaller screens */}
        <div className="flex flex-col w-4/5 lg:hidden">
          {steps.map((step, index) => (
            <GetStartedStep key={index} stepNumber={index + 1}>
              {step.content}
            </GetStartedStep>
          ))}
        </div>

        {/* Display the Carousel on large screens */}
        <div className="hidden lg:flex flex-col items-center justify-center w-4/5">
          <Carousel
            className="w-full shadow-[0_0_50px_-15px_rgba(0,0,0,0.2)] rounded-[20px] py-10 px-16 mt-10"
            autoPlay={false}
            navButtonsAlwaysVisible={true}
            height={500}
          >
            {steps.map((step, index) => (
              <GetStartedStep key={index} stepNumber={index + 1}>
                {step.content}
              </GetStartedStep>
            ))}
          </Carousel>
        </div>
      </div>
    </>
  )
}

export default GetStarted
