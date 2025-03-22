import { mount } from '@vue/test-utils'
import SearchBar from '@/components/SearchBar.vue'
import axios from 'axios'

vi.mock('axios')

describe('SearchBar.vue', () => {
  it('Renders correctly', () => {
    const wrapper = mount(SearchBar)
    expect(wrapper.exists()).toBe(true)
  })

  it('Updates input value', async () => {
    const wrapper = mount(SearchBar)
    const input = wrapper.find('input')
    await input.setValue('Test input')
    expect(wrapper.vm.input).toBe('Test input')
  })

  // Stubbing API calls
  // Reset all mocks before each test
  beforeEach(() => {
    vi.clearAllMocks()
  })

  // Mock API call
  it('Fetches data on mount', async () => {
    const mockTranscriptions = [
      { id: 1, title: 'Test 1', content: 'Content 1' },
      { id: 2, title: 'Test 2', content: 'Content 2' },
    ]

    vi.mocked(axios.get).mockResolvedValue({
      data: { transcriptions: mockTranscriptions },
    })

    const wrapper = mount(SearchBar)
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.transcriptions).toEqual(mockTranscriptions)
    expect(axios.get).toHaveBeenCalledWith(
      'http://127.0.0.1:5000/search?title='
    )
  })

  it('Searches for transcriptions when input changes', async () => {
    const mockTranscriptions = [
      { id: 1, title: 'Test 1', content: 'Content 1' },
    ]

    vi.mocked(axios.get).mockResolvedValue({
      data: { transcriptions: mockTranscriptions },
    })

    const wrapper = mount(SearchBar)

    const input = wrapper.find('#search-bar')
    await input.setValue('Test 1')

    await wrapper.vm.$nextTick()

    // Check if API was called with correct search term
    expect(axios.get).toHaveBeenCalledWith(
      'http://127.0.0.1:5000/search?title=Test 1'
    )

    expect(wrapper.vm.transcriptions).toEqual(mockTranscriptions)
  })
})
