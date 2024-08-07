import React from "react"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { faExternalLinkAlt } from "@fortawesome/free-solid-svg-icons"

const ExternalLink = ({ to, children }) => {
  return (
    <a
      href={to}
      target="_blank"
      rel="noopener noreferrer"
      className="text-sky-600 underline flex items-center"
    >
      {children}
      <FontAwesomeIcon icon={faExternalLinkAlt} className="ml-2" />
    </a>
  )
}

export default ExternalLink
