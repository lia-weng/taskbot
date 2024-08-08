import React from "react"

const GetStartedStep = ({ stepNumber, children }) => {
  return (
    <div className="flex flex-col items-center lg:text-left mt-10 w-full max-w-4xl">
      <h3 className="text-3xl text-sky-800 font-bold mt-5 mb-8">
        Step {stepNumber}:
      </h3>
      {children}
    </div>
  )
}

export default GetStartedStep
