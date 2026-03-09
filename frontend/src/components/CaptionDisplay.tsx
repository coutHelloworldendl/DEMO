import './CaptionDisplay.css'

interface CaptionDisplayProps {
  caption: string
  isLoading: boolean
}

function CaptionDisplay({ caption, isLoading }: CaptionDisplayProps) {
  if (!caption && !isLoading) {
    return (
      <div className="caption-display">
        <div className="empty-state">
          Upload an image and click "Generate Caption" to see AI-generated descriptions
        </div>
      </div>
    )
  }

  return (
    <div className="caption-display">
      <div className="caption-box">
        <div className="caption-label">
          {isLoading && <span className="loading-indicator"></span>}
          Caption:
        </div>
        <div className="caption-text">
          {caption || 'Generating caption...'}
        </div>
      </div>
    </div>
  )
}

export default CaptionDisplay
