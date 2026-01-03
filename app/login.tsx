'use client';
import { useState } from 'react';
import './styling.css';

export function Login( {onLogin}: {onLogin: () => void} ) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isSignedUp, setIsSignedUp] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        const endpoint = isSignedUp ? '/signup' : '/login';

        try {
            const res = await fetch(`http://localhost:8000${endpoint}`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({email, password})
            });

            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.detail || 'Authentication failed')
            }

            if (data.access_token) {
                localStorage.setItem('access_token', data.access_token);
                onLogin();
            }
        } catch (error: any) {
            setError(error.message);
            console.error('Auth failed', error);
        }
    }

    return (
        <div>
            <h1>{isSignedUp? 'Sign Up' : 'Login'}</h1>
            <form onSubmit={handleSubmit}>

                {/* div for email input */}
                <div>
                    <input
                        type="email"
                        placeholder="Email"
                        className="input_box"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>

                {/* div for password input */}
                <div>
                    <input
                        type="password"
                        placeholder="Password"
                        className="input_box"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>

                {/* button to submit details */}
                <button type="submit">
                    {isSignedUp? 'Sign up' : 'Login'}
                </button>
            </form>

            <p>
                {isSignedUp? 'Already have an account?' : 'Don\'t have an account?'}
                <button onClick={() => setIsSignedUp(!isSignedUp)}>
                    {isSignedUp? 'Login': 'Sign Up'}
                </button>
            </p>
        </div>
    )
}

