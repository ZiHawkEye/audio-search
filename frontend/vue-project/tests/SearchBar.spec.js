import { mount } from '@vue/test-utils'
import SearchBar from '@/components/SearchBar.vue'

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
  //   describe('SearchBar.vue', () => {
  //     it('fetches data on mount', async () => {
  //       const mockData = { transcriptions: 'some data' }
  //       axios.get.mockResolvedValue(mockData) // Mock API response

  //       const wrapper = mount(SearchBar)
  //       await wrapper.vm.$nextTick() // Wait for the component to update

  //       expect(wrapper.vm.data).toEqual(mockData.data) // Check if data is set correctly
  //     })
  //    })
})
