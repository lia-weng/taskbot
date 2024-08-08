import React from "react"
import { useEffect, useState } from "react"
import Cookies from "js-cookie"
import { Link } from "react-router-dom"

import { GoogleLogin } from "./Button"
import GetStartedStep from "./GetStartedStep"
import ExternalLink from "./ExternalLink"
import taskListImg from "../images/task-list.png"
import addTaskImg from "../images/add-tasks.jpg"

const baseURL = "https://oyster-ace-sturgeon.ngrok-free.app"

const GetStarted = () => {
  const [loggedIn, setLoggedIn] = useState(false)

  useEffect(() => {
    const authCookie = Cookies.get("authenticated")

    if (authCookie === "true") {
      setLoggedIn(true)
    } else {
      setLoggedIn(false)
    }
    console.log(loggedIn)
  }, [loggedIn])

  const steps = [
    {
      content: loggedIn ? (
        <p className="text-xl text-gray-600 font-semibold mb-5 lg:mb-0 lg:mr-5">
          Connected to: {Cookies.get("email")}
        </p>
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
          <p className="text-xl text-gray-600 font-semibold flex flex-row">
            Go to &nbsp;
            <ExternalLink to="https://tasks.google.com/">
              Google Tasks
            </ExternalLink>
            &nbsp;&nbsp;You will see a task list called "taskbot".
          </p>
          <img
            src={taskListImg}
            alt="Task list called 'taskbot'"
            className="mt-5 w-full max-w-4xl drop-shadow-md"
          />
        </>
      ),
    },
    {
      content: (
        <>
          <p className="text-xl text-gray-600 font-semibold">
            Add some tasks to "taskbot".
          </p>
          <img
            src={addTaskImg}
            alt="Add some tasks to 'taskbot'"
            className="mt-5 w-full lg:w-fit max-w-4xl drop-shadow-md"
          />
        </>
      ),
    },
    {
      content: (
        <>
          <p className="text-xl text-gray-600 font-semibold">
            Enter your phone number. This will be the number taskbot uses to
            send you reminders.
          </p>
        </>
      ),
    },
    {
      content: (
        <>
          <p className="text-xl text-gray-600 font-semibold">
            You're all set! Taskbot will send you reminders and let you manage
            your tasks through text messages.
          </p>
        </>
      ),
    },
  ]

  return (
    <>
      <div
        className="flex flex-col py-16 lg:py-20 px-14 items-center"
        id="get-started"
        data-aos="fade-up"
        data-aos-delay="500"
      >
        <h2 className="mb-5 text-center text-3xl text-sky-800 font-bold underline underline-offset-8">
          Get Started
        </h2>

        {steps.map((step, index) => (
          <GetStartedStep key={index} stepNumber={index + 1}>
            {step.content}
          </GetStartedStep>
        ))}
      </div>
    </>
  )
}

export default GetStarted
