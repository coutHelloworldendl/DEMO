import { useState, useEffect } from 'react'
import ImageUpload from './components/ImageUpload'
import ModelSelector from './components/ModelSelector'
import CaptionDisplay from './components/CaptionDisplay'
import './App.css'

interface Model {
  id: string
  name: string
  provider: string
  supports_streaming: boolean
}

function App() {
  const [models, setModels] = useState<Model[]>([])
  const [selectedModel, setSelectedModel] = useState<string>('')
  const [selectedImage, setSelectedImage] = useState<File | null>(null)
  const [imagePreview, setImagePreview] = useState<string>('')
  const [caption, setCaption] = useState<string>('')
  const [isLoading, setIsLoading] = useState<boolean>(false)

  useEffect(() => {
    fetchModels()
  }, [])

  const fetchModels = async () => {
    try {
      const response = await fetch('/api/models')
      const data = await response.json()
      setModels(data.models)
      if (data.models.length > 0) {
        setSelectedModel(data.models[0].id)
      }
    } catch (error) {
      console.error('Error fetching models:', error)
    }
  }

  const handleImageSelect = (file: File) => {
    setSelectedImage(file)
    const reader = new FileReader()
    reader.onloadend = () => {
      setImagePreview(reader.result as string)
    }
    reader.readAsDataURL(file)
    setCaption('')
  }

  const handleGenerateCaption = async () => {
    if (!selectedImage || !selectedModel) return

    setIsLoading(true)
    setCaption('')

    try {
      const formData = new FormData()
      formData.append('file', selectedImage)
      formData.append('model_id', selectedModel)
      formData.append('stream', 'true')

      const response = await fetch('/api/caption', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Failed to generate caption')
      }

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()

      if (reader) {
        let accumulatedCaption = ''
        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          const chunk = decoder.decode(value)
          const lines = chunk.split('\n')

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const text = line.slice(6)
              accumulatedCaption += text
              setCaption(accumulatedCaption)
            }
          }
        }
      }
    } catch (error) {
      console.error('Error generating caption:', error)
      setCaption('Error generating caption. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <h1 className="title">🖼️ Image Captioning Demo</h1>
        <p className="subtitle">Upload an image and let AI describe it for you</p>

        <ModelSelector
          models={models}
          selectedModel={selectedModel}
          onModelChange={setSelectedModel}
        />

        <ImageUpload
          onImageSelect={handleImageSelect}
          imagePreview={imagePreview}
        />

        {selectedImage && (
          <button
            className="generate-btn"
            onClick={handleGenerateCaption}
            disabled={isLoading}
          >
            {isLoading ? 'Generating...' : 'Generate Caption'}
          </button>
        )}

        <CaptionDisplay caption={caption} isLoading={isLoading} />
      </div>
    </div>
  )
}

export default App
