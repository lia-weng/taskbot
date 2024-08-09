import React from "react"

const GetStartedStep = ({ stepNumber, children }) => {
  return (
    <div className="flex flex-col items-center w-full h-full mx-auto overflow-hidden my-5 lg:my-0">
      <h3 className="text-3xl text-sky-800 font-bold mb-8">
        Step {stepNumber}
      </h3>
      {children}
    </div>
  )
}

export default GetStartedStep
