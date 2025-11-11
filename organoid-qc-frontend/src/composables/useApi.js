import axios from "axios";
import { ref } from "vue";
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// Global loading and error states
const isLoading = ref(false);
const apiError = ref(null);

// Create axios instance with defaults
const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    
  }
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    isLoading.value = true;
    apiError.value = null;
    return config;
  },
  (error) => {
    isLoading.value = false;
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    isLoading.value = false;
    apiError.value = null;
    
    // Set Content-Type for non-FormData requests
    if (!(response.data instanceof FormData)) {
      response.headers["Content-Type"] = "application/json";
    }
    return response;
  },
  (error) => {
    isLoading.value = false;

    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      const data = error.response.data;

      console.error("🔴 API Error:", data);

      switch (status) {
        case 400:
          apiError.value = data.detail || "Invalid request";
          break;
        case 404:
          apiError.value = "Resource not found";
          break;
        case 409:
          apiError.value = "Conflict - resource already exists";
          break;
        case 422:
          // Unpack validation error
          if (data.detail) {
            console.error("Validation error:", data.detail);  // ← ADD THIS
            apiError.value = JSON.stringify(data.detail);
          }
          break;
        case 500:
          apiError.value = "Server error - please try again later";
          break;
        default:
          apiError.value = data.detail || `Error: ${status}`;
      }
    } else if (error.request) {
      // Request made but no response
      apiError.value = "No response from server - check your connection";
    } else {
      // Error in request setup
      apiError.value = error.message || "Unknown error occurred";
    }

    return Promise.reject(error);
  }
);

/**
 * Generic GET request
 */
const get = async (url, config = {}) => {
  try {
    const response = await apiClient.get(url, config);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Generic POST request
 */
const post = async (url, data = {}, config = {}) => {
  try {
    const response = await apiClient.post(url, data, config);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Generic PUT request
 */
const put = async (url, data = {}, config = {}) => {
  try {
    const response = await apiClient.put(url, data, config);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Generic PATCH request
 */
const patch = async (url, data = {}, config = {}) => {
  try {
    const response = await apiClient.patch(url, data, config);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Generic DELETE request
 */
const del = async (url, config = {}) => {
  try {
    const response = await apiClient.delete(url, config);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * Upload file
 */
const uploadFile = async (url, file, additionalData = {}, onProgress = null) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    // Add additional form data
    Object.entries(additionalData).forEach(([key, value]) => {
      if (value) formData.append(key, value);
    });

    const config = {};  

    if (onProgress) {
      config.onUploadProgress = (progressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        onProgress(percentCompleted);
      };
    }

    return await post(url, formData, config);
  } catch (error) {
    throw error;
  }
};

/**
 * Clear error
 */
const clearError = () => {
  apiError.value = null;
};

/**
 * Check if API is available
 */
const checkHealth = async () => {
  try {
    // Try a simple request to verify API is reachable
    await get("/experiments");
    return true;
  } catch (error) {
    console.error("API health check failed:", error);
    return false;
  }
};

export function useApi() {
  return {
    // State
    isLoading,
    apiError,
    apiClient,

    // Methods
    get,
    post,
    put,
    patch,
    del,
    uploadFile,
    clearError,
    checkHealth,

    // Constants
    API_URL
  };
}