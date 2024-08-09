import React from "react"

const GetStartedStep = ({ stepNumber, children }) => {
  return (
    <div className="flex flex-col items-center py-5 w-full mx-auto">
      <h3 className="text-3xl text-sky-800 font-bold mb-8">
        Step {stepNumber}
      </h3>
      {children}
    </div>
  )
}

export default GetStartedStep
