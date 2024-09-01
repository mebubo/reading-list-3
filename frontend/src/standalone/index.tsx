import React, { useEffect } from "react"
import { createRoot } from 'react-dom/client'

const container = document.getElementById('app')

const root = createRoot(container!)

function Hello() {
  useEffect(() => {
    console.log('rendered')
  });

  return <div>Hello</div>
}

root.render(<Hello />)