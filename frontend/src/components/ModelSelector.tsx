import './ModelSelector.css'

interface Model {
  id: string
  name: string
  provider: string
  supports_streaming: boolean
}

interface ModelSelectorProps {
  models: Model[]
  selectedModel: string
  onModelChange: (modelId: string) => void
}

function ModelSelector({ models, selectedModel, onModelChange }: ModelSelectorProps) {
  return (
    <div className="model-selector">
      <label htmlFor="model-select">Select AI Model:</label>
      <select
        id="model-select"
        value={selectedModel}
        onChange={(e) => onModelChange(e.target.value)}
      >
        {models.map((model) => (
          <option key={model.id} value={model.id}>
            {model.name} ({model.provider})
          </option>
        ))}
      </select>
    </div>
  )
}

export default ModelSelector
