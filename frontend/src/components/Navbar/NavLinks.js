import React from "react"
import { HashLink } from "react-router-hash-link"
import { Link } from "react-router-dom"

const NavLinks = () => {
  return (
    <>
      <HashLink
        className="big-text hover:text-sky-800 px-4"
        smooth
        to="/#get-started"
      >
        Get Started
      </HashLink>
      <a
        href={"https://github.com/lia-weng/taskbot"}
        target="_blank"
        rel="noopener noreferrer"
        className="big-text hover:text-sky-800 px-4"
      >
        Github
      </a>
      <a
        className="big-text hover:text-sky-800 px-4"
        href="mailto:lia.xin.weng@gmail.com"
        target="_blank"
        rel="noopener noreferrer"
      >
        Contact
      </a>
    </>
  )
}

export default NavLinks
