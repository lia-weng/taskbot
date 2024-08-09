import React from "react"
import Paper from "@mui/material/Paper"
import Carousel from "react-material-ui-carousel"

const GetStartedStep = ({ stepNumber, children }) => {
  return (
    <div className="flex flex-col items-center w-full h-full mx-auto overflow-hidden my-0">
      <h3 className="subtitle mb-4 lg:mb-8">Step {stepNumber}</h3>
      {children}
    </div>
  )
}

const GetStartedDisplay = ({ steps }) => {
  return (
    <>
      {/* Display the steps on smaller screens */}
      <div className="flex flex-col w-4/5 lg:hidden">
        {steps.map((step, index) => (
          <Paper elevation={2} className="my-4 p-5">
            <GetStartedStep key={index} stepNumber={index + 1}>
              {step.content}
            </GetStartedStep>
          </Paper>
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
    </>
  )
}

export default GetStartedDisplay
