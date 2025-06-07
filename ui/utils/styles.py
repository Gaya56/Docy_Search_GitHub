"""
CSS Styles for Docy Search Assistant UI
Contains all custom styling for the Streamlit interface
"""

def get_main_styles() -> str:
    """
    Get the main CSS styles for the application
    
    Returns:
        String containing CSS styles for injection into Streamlit
    """
    return """
    <style>
        .main-header {
            background: linear-gradient(90deg, #1f77b4, #ff7f0e);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .activity-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .cost-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .memory-card {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .tool-card {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 0.8rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            border: 1px solid #e0e0e0;
            transition: all 0.3s ease;
        }
        
        .tool-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }
        
        .model-selector {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            border: 1px solid #e0e0e0;
        }
        
        .configuration-banner {
            background: linear-gradient(90deg, #74b9ff, #0984e3);
            color: white;
            padding: 0.8rem;
            border-radius: 8px;
            margin: 1rem 0;
            text-align: center;
            font-weight: 500;
        }
        
        .chat-message {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 10px;
            border-left: 4px solid #74b9ff;
            background-color: #f8f9fa;
        }
        
        .user-message {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            border-left-color: #2196f3;
        }
        
        .assistant-message {
            background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
            border-left-color: #9c27b0;
        }
        
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-active {
            background-color: #4caf50;
            animation: pulse 2s infinite;
        }
        
        .status-inactive {
            background-color: #f44336;
        }
        
        .status-warning {
            background-color: #ff9800;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        
        .metric-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #7f8c8d;
            margin-top: 0.25rem;
        }
        
        .footer-caption {
            text-align: center;
            color: #7f8c8d;
            font-size: 0.8rem;
            padding: 0.5rem;
            margin: 0.5rem 0;
        }
        
        .maintenance-button {
            background: linear-gradient(135deg, #fd79a8 0%, #fdcb6e 100%);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .maintenance-button:hover {
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        .sidebar-section {
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .sidebar-section:last-child {
            border-bottom: none;
        }
        
        .sidebar-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 0.8rem;
            display: flex;
            align-items: center;
        }
        
        .sidebar-title::before {
            content: "";
            display: inline-block;
            width: 4px;
            height: 20px;
            background: linear-gradient(180deg, #74b9ff, #0984e3);
            margin-right: 8px;
            border-radius: 2px;
        }
        
        /* Responsive design improvements */
        @media (max-width: 768px) {
            .main-header {
                font-size: 2rem;
            }
            
            .activity-card, .cost-card, .memory-card {
                padding: 0.8rem;
            }
            
            .configuration-banner {
                padding: 0.6rem;
                font-size: 0.9rem;
            }
        }
        
        /* Streamlit specific overrides */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }
        
        .stSelectbox > label {
            font-weight: 600;
            color: #2c3e50;
        }
        
        .stCheckbox > label {
            font-weight: 500;
            color: #34495e;
        }
        
        /* Custom scrollbar for sidebar */
        .css-1d391kg {
            scrollbar-width: thin;
            scrollbar-color: #74b9ff #f1f3f4;
        }
        
        .css-1d391kg::-webkit-scrollbar {
            width: 6px;
        }
        
        .css-1d391kg::-webkit-scrollbar-track {
            background: #f1f3f4;
        }
        
        .css-1d391kg::-webkit-scrollbar-thumb {
            background: #74b9ff;
            border-radius: 3px;
        }
        
        .css-1d391kg::-webkit-scrollbar-thumb:hover {
            background: #0984e3;
        }
    </style>
    """


def get_chat_styles() -> str:
    """
    Get specific CSS styles for the chat interface
    
    Returns:
        String containing chat-specific CSS styles
    """
    return """
    <style>
        .chat-container {
            max-height: 600px;
            overflow-y: auto;
            padding: 1rem;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        .chat-input-container {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            border: 2px solid #e9ecef;
            margin-bottom: 1rem;
            transition: border-color 0.3s ease;
        }
        
        .chat-input-container:focus-within {
            border-color: #74b9ff;
        }
        
        .chat-response-container {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #e9ecef;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
        
        .thinking-indicator {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
            color: #74b9ff;
            font-style: italic;
        }
        
        .thinking-dots {
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background-color: #74b9ff;
            margin: 0 2px;
            animation: thinking 1.4s infinite ease-in-out both;
        }
        
        .thinking-dots:nth-child(1) { animation-delay: -0.32s; }
        .thinking-dots:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes thinking {
            0%, 80%, 100% { 
                transform: scale(0);
                opacity: 0.5;
            } 
            40% { 
                transform: scale(1);
                opacity: 1;
            }
        }
        
        .memory-status-success {
            color: #28a745;
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }
        
        .memory-status-info {
            color: #17a2b8;
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }
        
        .chat-timestamp {
            color: #6c757d;
            font-size: 0.75rem;
            margin-top: 0.5rem;
            text-align: right;
        }
    </style>
    """


def get_sidebar_styles() -> str:
    """
    Get specific CSS styles for the sidebar
    
    Returns:
        String containing sidebar-specific CSS styles
    """
    return """
    <style>
        .sidebar-metric {
            background: rgba(255, 255, 255, 0.1);
            padding: 0.8rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .sidebar-metric-value {
            font-size: 1.2rem;
            font-weight: bold;
            color: white;
        }
        
        .sidebar-metric-label {
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.8);
            margin-top: 0.25rem;
        }
        
        .tool-selection-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 0.5rem;
            margin: 1rem 0;
        }
        
        .tool-checkbox {
            background: rgba(255, 255, 255, 0.95);
            padding: 0.8rem;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .tool-checkbox:hover {
            background: rgba(255, 255, 255, 1);
            transform: translateX(2px);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .tool-checkbox.selected {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            border-color: #2196f3;
        }
        
        .model-selection-container {
            background: rgba(255, 255, 255, 0.95);
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            border: 1px solid #e0e0e0;
        }
        
        .maintenance-section {
            background: linear-gradient(135deg, #ff7675 0%, #fd79a8 100%);
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            color: white;
        }
        
        .maintenance-section h4 {
            color: white;
            margin-bottom: 0.8rem;
        }
        
        .maintenance-warning {
            background: rgba(255, 255, 255, 0.2);
            padding: 0.6rem;
            border-radius: 6px;
            margin: 0.5rem 0;
            font-size: 0.85rem;
            border-left: 3px solid rgba(255, 255, 255, 0.5);
        }
    </style>
    """


def get_responsive_styles() -> str:
    """
    Get responsive CSS styles for mobile and tablet devices
    
    Returns:
        String containing responsive CSS styles
    """
    return """
    <style>
        /* Mobile First Approach */
        @media (max-width: 576px) {
            .main-header {
                font-size: 1.8rem;
                margin-bottom: 1rem;
            }
            
            .activity-card, .cost-card, .memory-card {
                padding: 0.6rem;
                margin-bottom: 0.8rem;
            }
            
            .configuration-banner {
                padding: 0.5rem;
                font-size: 0.8rem;
            }
            
            .chat-response-container {
                padding: 1rem;
                margin: 0.8rem 0;
            }
            
            .sidebar-section {
                margin-bottom: 1rem;
                padding-bottom: 0.8rem;
            }
        }
        
        /* Tablet Styles */
        @media (min-width: 577px) and (max-width: 768px) {
            .main-header {
                font-size: 2.2rem;
            }
            
            .tool-selection-grid {
                grid-template-columns: 1fr 1fr;
                gap: 0.8rem;
            }
        }
        
        /* Desktop Styles */
        @media (min-width: 769px) {
            .tool-selection-grid {
                grid-template-columns: 1fr;
            }
            
            .chat-container {
                max-height: 700px;
            }
        }
        
        /* Large Desktop Styles */
        @media (min-width: 1200px) {
            .main-header {
                font-size: 3rem;
            }
            
            .chat-container {
                max-height: 800px;
            }
        }
    </style>
    """


def inject_all_styles() -> None:
    """
    Inject all CSS styles into the Streamlit app
    This should be called once in the main application
    """
    import streamlit as st
    
    # Combine all styles
    all_styles = (
        get_main_styles() + 
        get_chat_styles() + 
        get_sidebar_styles() + 
        get_responsive_styles()
    )
    
    # Inject into Streamlit
    st.markdown(all_styles, unsafe_allow_html=True)
