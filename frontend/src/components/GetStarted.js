import React from "react"
import { useEffect, useState } from "react"
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
import addTaskImg from "../images/add-tasks.jpg"

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
    if (!phoneNumber) {
      setPhoneNumberError("Please enter a valid phone number.")
    } else if (isPossiblePhoneNumber(phoneNumber) === false) {
      setPhoneNumberError("Please enter a valid phone number.")
    } else {
      setPhoneNumberError()
      setPhoneNumberComplete(true)
    }

    // try {
    //   // Replace with your backend endpoint
    //   await axios.post("/api/submit-phone", { phoneNumber })
    //   // Handle successful submission here, e.g., show a success message
    // } catch (error) {
    //   // Handle errors here
    //   console.error("Error submitting phone number:", error)
    // }
  }

  const steps = [
    {
      content: loggedIn ? (
        <p className="big-text">Connected to: {Cookies.get("email")}</p>
      ) : (
        <GoogleLogin
          onClick={() => (window.open = `${baseURL}/authorize`)}
          label={"Connect your Google account"}
        />
      ),
    },
    {
      content: (
        <>
          <p className="big-text">
            Go to &nbsp;
            {/* <span>
              <ExternalLink to="https://tasks.google.com/">
                Google Tasks
              </ExternalLink>
            </span> */}
            <a
              href={"https://tasks.google.com/"}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sky-600 underline"
            >
              Google Tasks
            </a>
            . You will see a task list called "taskbot".
          </p>
          <img
            src={taskListImg}
            alt="Task list called 'taskbot'"
            className="mt-5 w-full drop-shadow-md"
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
            className="mt-5 w-full max-w-4xl drop-shadow-md"
          />
        </>
      ),
    },
    {
      content: (
        <>
          {phoneNumberComplete ? (
            <>
              <p className="big-text">Awesome! Taskbot will text you at:</p>
              <div className="flex-col items-center mt-8">
                <PhoneInput
                  international
                  defaultCountry="CA"
                  placeholder="Enter phone number"
                  value={phoneNumber}
                  onChange={setPhoneNumber}
                  className="text-xl text-gray-600 font-semibold mb-8"
                />
                <IconButton
                  aria-label="Edit number"
                  color="secondary"
                  onClick={() => setPhoneNumberComplete(false)}
                  sx={{ display: "none" }}
                >
                  <EditIcon />
                </IconButton>
                <Button
                  variant="contained"
                  color="secondary"
                  onClick={() => setPhoneNumberComplete(false)}
                >
                  Change
                </Button>
              </div>
            </>
          ) : (
            <>
              <p className="big-text">Enter your phone number.</p>
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
                <Button variant="contained" color="secondary" type="submit">
                  Confirm
                </Button>
              </form>
              {phoneNumberError ? (
                <Alert severity="error" className="mt-8">
                  {phoneNumberError}
                </Alert>
              ) : (
                <></>
              )}
            </>
          )}
        </>
      ),
    },
    {
      content: (
        <>
          <p className="big-text">You're all set!</p>
          <p className="big-text">
            Taskbot will send you reminders and let you manage your tasks
            through text.
          </p>
        </>
      ),
    },
  ]

  return (
    <>
      <div
        className="flex flex-col py-16 lg:py-20 px-14 items-center text-center"
        id="get-started"
        data-aos="fade-up"
        data-aos-delay="500"
      >
        <h2 className="mb-5 text-center text-3xl text-sky-800 font-bold underline underline-offset-8">
          Get Started
        </h2>

        {/* Display the steps on smaller screens */}
        <div className="flex flex-col lg:hidden">
          {steps.map((step, index) => (
            <GetStartedStep key={index} stepNumber={index + 1}>
              {step.content}
            </GetStartedStep>
          ))}
        </div>

        {/* Display the Carousel on large screens */}
        <div className="hidden lg:flex flex-col items-center justify-center w-4/5 py-5 px-20">
          <Carousel
            className="w-full"
            autoPlay={false}
            navButtonsAlwaysVisible={true}
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
