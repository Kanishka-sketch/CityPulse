const API_BASE_URL = "http://127.0.0.1:8000";

export async function getHealth() {
    const response = await fetch(`${API_BASE_URL}/api/health`);

    if (!response.ok) {
        throw new Error("Failed to fetch health data");
    }

    return response.json();
}

export async function getInsight() {
    const response = await fetch(`${API_BASE_URL}/api/insight`);

    if (!response.ok) {
        throw new Error("Failed to fetch insight");
    }

    return response.json();
}

export async function getLatest() {
    const response = await fetch(`${API_BASE_URL}/api/latest`);

    if (!response.ok) {
        throw new Error("Failed to fetch latest data");
    }

    return response.json();
}

export async function getAnomalies() {
    const response = await fetch(`${API_BASE_URL}/api/anomalies`);

    if (!response.ok) {
        throw new Error("Failed to fetch anomalies");
    }

    return response.json();
}