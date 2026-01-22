import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { getCookie, deleteCookie } from 'cookies-next';

// --- Interfaces ---

export interface User {
    id: string;
    email: string;
    business_type?: string | null;
    auth_provider: string;
}

export interface TokenResponse {
    access_token: string;
    token_type: string;
    user_id: string;
}

export interface DashboardSummary {
    total_income: number;
    total_expense: number;
    net_profit: number;
    savings_rate: number;
}

export interface ChartPoint {
    date: string;
    income: number;
    expense: number;
    net_change: number;
    // other props can be added if needed
}

export interface TopExpense {
    category: string;
    amount: number;
    percentage: number;
}

export interface DashboardData {
    current_balance: number;
    growth_percentage: number;
    top_expenses: TopExpense[];
    summary: DashboardSummary;
    charts: ChartPoint[];
    details: {
        income_by_category: { category: string; amount: number; percentage: number }[];
        expense_by_category: { category: string; amount: number; percentage: number }[];
        avg_stats?: {
            daily_income: number;
            daily_expense: number;
        };
    };
}

export interface DashboardResponse {
    success: boolean;
    data: DashboardData;
}

export interface Transaction {
    id: string;
    date: string;
    amount: number;
    description: string;
    category?: string;
    is_expense: boolean;
    is_fixed: boolean;
}

// --- API Service ---

class ApiService {
    private client: AxiosInstance;

    constructor() {
        this.client = axios.create({
            baseURL: '/api', // Proxy URL
            headers: {
                'Content-Type': 'application/json',
            },
        });

        // Interceptors
        this.client.interceptors.request.use(
            (config) => {
                const token = getCookie('access_token');
                if (token) {
                    config.headers.Authorization = `Bearer ${token}`;
                }
                return config;
            },
            (error) => Promise.reject(error)
        );

        this.client.interceptors.response.use(
            (response) => response,
            (error) => {
                if (error.response?.status === 401) {
                    deleteCookie('access_token');
                    if (typeof window !== 'undefined') {
                        window.location.href = '/login';
                    }
                }
                return Promise.reject(error);
            }
        );
    }

    // Generic GET, POST, etc (to expose underlying axios if needed)
    public get = <T = any, R = AxiosResponse<T>, D = any>(url: string, config?: any) => this.client.get<T, R, D>(url, config);
    public post = <T = any, R = AxiosResponse<T>, D = any>(url: string, data?: D, config?: any) => this.client.post<T, R, D>(url, data, config);
    public put = <T = any, R = AxiosResponse<T>, D = any>(url: string, data?: D, config?: any) => this.client.put<T, R, D>(url, data, config);
    public delete = <T = any, R = AxiosResponse<T>, D = any>(url: string, config?: any) => this.client.delete<T, R, D>(url, config);
    public patch = <T = any, R = AxiosResponse<T>, D = any>(url: string, data?: D, config?: any) => this.client.patch<T, R, D>(url, data, config);

    // --- Dashboard Methods ---

    public async getDashboard(filterType: string = 'this_month'): Promise<DashboardResponse> {
        const response = await this.client.get<DashboardResponse>(`/analytics/dashboard?filter_type=${filterType}`);
        return response.data;
    }

    public async getTransactions(page: number = 1, limit: number = 50, search: string = ''): Promise<{ items: Transaction[], total: number }> {
        const response = await this.client.get(`/data/transactions?page=${page}&limit=${limit}&search=${search}`);
        return response.data;
    }

    public async getFilterOptions(): Promise<{ categories: string[], min_amount: number, max_amount: number }> {
        const response = await this.client.get('/analytics/filters');
        return response.data;
    }

    // Add other methods as needed
}

const api = new ApiService();
export default api;
