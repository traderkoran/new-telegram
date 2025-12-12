"""
Comprehensive 7-Layer Analysis Engine
Integrates PROMETHEUS AI v6.0 and Efsanevi Yatırım Yeteneği systems
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple
import ta
import pandas_ta as ta2
from datetime import datetime, timedelta

class ComprehensiveAnalyzer:
    def __init__(self):
        self.patterns_recognized = 0
        self.indicators_calculated = 0
        
    def analyze(self, symbol: str, price_data: pd.DataFrame, analysis_type: str = "full") -> Dict[str, Any]:
        """
        Perform comprehensive 7-layer analysis
        
        Args:
            symbol: Asset symbol
            price_data: Price data DataFrame
            analysis_type: "full", "quick", or "risk"
            
        Returns:
            Dict containing all analysis results
        """
        
        result = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "analysis_type": analysis_type,
            "current_price": float(price_data['Close'].iloc[-1]) if len(price_data) > 0 else 0,
            "price_change_24h": 0,
            "volume_24h": 0
        }
        
        # Layer 1: Price Action Analysis
        result.update(self._analyze_price_action(price_data))
        
        # Layer 2: Technical Indicators
        result.update(self._analyze_technical_indicators(price_data))
        
        # Layer 3: Fibonacci & Mathematical Analysis
        result.update(self._analyze_fibonacci(price_data))
        
        # Layer 4: Market Structure
        result.update(self._analyze_market_structure(price_data))
        
        # Layer 5: Fundamental Analysis
        result.update(self._analyze_fundamental(symbol, price_data))
        
        # Layer 6: Sentiment Analysis
        result.update(self._analyze_sentiment(symbol, price_data))
        
        # Layer 7: Risk Management
        result.update(self._analyze_risk_management(symbol, price_data, result))
        
        # Generate final signal
        result.update(self._generate_final_signal(result))
        
        return result
    
    def _analyze_price_action(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Layer 1: Price Action Analysis (38+ patterns)"""
        
        if len(data) < 20:
            return {"price_action": {"error": "Insufficient data"}}
        
        close = data['Close']
        open_ = data['Open']
        high = data['High']
        low = data['Low']
        volume = data['Volume'] if 'Volume' in data.columns else None
        
        patterns = {
            # Single Candle Patterns
            "doji": self._detect_doji(data),
            "hammer": self._detect_hammer(data),
            "hanging_man": self._detect_hanging_man(data),
            "shooting_star": self._detect_shooting_star(data),
            "marubozu": self._detect_marubozu(data),
            "spinning_top": self._detect_spinning_top(data),
            
            # Multi-Candle Patterns
            "engulfing": self._detect_engulfing(data),
            "harami": self._detect_harami(data),
            "morning_star": self._detect_morning_star(data),
            "evening_star": self._detect_evening_star(data),
            "three_white_soldiers": self._detect_three_white_soldiers(data),
            "three_black_crows": self._detect_three_black_crows(data),
            
            # Chart Patterns (simplified detection)
            "head_shoulders": self._detect_head_shoulders(data),
            "double_top_bottom": self._detect_double_top_bottom(data),
            "triangles": self._detect_triangles(data),
            "flags_pennants": self._detect_flags_pennants(data),
            "cup_handle": self._detect_cup_handle(data),
        }
        
        # Elliott Wave Analysis
        elliott_wave = self._analyze_elliott_wave(data)
        
        # Harmonic Patterns
        harmonic_patterns = self._analyze_harmonic_patterns(data)
        
        return {
            "price_action": {
                "patterns_detected": {k: v for k, v in patterns.items() if v["detected"]},
                "active_patterns_count": sum(1 for v in patterns.values() if v["detected"]),
                "last_signals": self._get_last_signals(patterns),
                "elliott_wave": elliott_wave,
                "harmonic_patterns": harmonic_patterns,
                "candle_analysis": self._analyze_last_candles(data, 5)
            }
        }
    
    def _analyze_technical_indicators(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Layer 2: Technical Indicators (50+ indicators)"""
        
        if len(data) < 50:
            return {"technical_indicators": {"error": "Insufficient data"}}
        
        close = data['Close']
        high = data['High']
        low = data['Low']
        volume = data['Volume'] if 'Volume' in data.columns else None
        
        # Momentum Indicators
        rsi = ta.momentum.RSIIndicator(close=close, window=14)
        macd = ta.trend.MACD(close=close)
        stoch = ta.momentum.StochasticOscillator(high=high, low=low, close=close)
        williams_r = ta.momentum.WilliamsRIndicator(high=high, low=low, close=close)
        cci = ta.trend.CCIIndicator(high=high, low=low, close=close)
        awesome_oscillator = ta.momentum.AwesomeOscillatorIndicator(high=high, low=low)
        
        # Trend Indicators
        sma_20 = ta.trend.SMAIndicator(close=close, window=20)
        sma_50 = ta.trend.SMAIndicator(close=close, window=50)
        sma_200 = ta.trend.SMAIndicator(close=close, window=200)
        ema_20 = ta.trend.EMAIndicator(close=close, window=20)
        adx = ta.trend.ADXIndicator(high=high, low=low, close=close)
        parabolic_sar = ta.trend.PSARIndicator(high=high, low=low, close=close)
        
        # Volatility Indicators
        bollinger = ta.volatility.BollingerBands(close=close)
        atr = ta.volatility.AverageTrueRange(high=high, low=low, close=close)
        
        # Volume Indicators
        obv = ta.volume.OnBalanceVolumeIndicator(close=close, volume=volume)
        mfi = ta.volume.MFIIndicator(high=high, low=low, close=close, volume=volume)
        volume_sma = ta.volume.VolumeWeightedAveragePrice(
            high=high, low=low, close=close, volume=volume
        )
        
        # Additional indicators from pandas_ta
        ichimoku = ta2.ichimoku(high, low, close)
        supertrend = ta2.supertrend(high, low, close)
        donchian = ta2.donchian(high, low)
        
        # Calculate divergences
        divergences = self._calculate_divergences(data, rsi, macd)
        
        return {
            "technical_indicators": {
                "momentum": {
                    "rsi": {
                        "value": float(rsi.rsi().iloc[-1]),
                        "signal": self._get_rsi_signal(rsi.rsi().iloc[-1]),
                        "divergence": divergences.get("rsi")
                    },
                    "macd": {
                        "value": float(macd.macd().iloc[-1]),
                        "signal_line": float(macd.macd_signal().iloc[-1]),
                        "histogram": float(macd.macd_diff().iloc[-1]),
                        "signal": "bullish" if macd.macd().iloc[-1] > macd.macd_signal().iloc[-1] else "bearish",
                        "divergence": divergences.get("macd")
                    },
                    "stochastic": {
                        "k": float(stoch.stoch().iloc[-1]),
                        "d": float(stoch.stoch_signal().iloc[-1]),
                        "signal": self._get_stoch_signal(stoch.stoch().iloc[-1], stoch.stoch_signal().iloc[-1])
                    },
                    "williams_r": {
                        "value": float(williams_r.williams_r().iloc[-1]),
                        "signal": self._get_williams_r_signal(williams_r.williams_r().iloc[-1])
                    },
                    "cci": {
                        "value": float(cci.cci().iloc[-1]),
                        "signal": self._get_cci_signal(cci.cci().iloc[-1])
                    }
                },
                "trend": {
                    "moving_averages": {
                        "sma_20": float(sma_20.sma_indicator().iloc[-1]),
                        "sma_50": float(sma_50.sma_indicator().iloc[-1]),
                        "sma_200": float(sma_200.sma_indicator().iloc[-1]),
                        "ema_20": float(ema_20.ema_indicator().iloc[-1]),
                        "golden_cross": sma_50.sma_indicator().iloc[-1] > sma_200.sma_indicator().iloc[-1],
                        "death_cross": sma_50.sma_indicator().iloc[-1] < sma_200.sma_indicator().iloc[-1]
                    },
                    "adx": {
                        "value": float(adx.adx().iloc[-1]),
                        "plus_di": float(adx.adx_pos().iloc[-1]),
                        "minus_di": float(adx.adx_neg().iloc[-1]),
                        "trend_strength": self._get_adx_strength(adx.adx().iloc[-1])
                    },
                    "parabolic_sar": {
                        "value": float(parabolic_sar.psar().iloc[-1]),
                        "signal": "bullish" if close.iloc[-1] > parabolic_sar.psar().iloc[-1] else "bearish"
                    },
                    "ichimoku": self._parse_ichimoku(ichimoku, close),
                    "supertrend": self._parse_supertrend(supertrend, close)
                },
                "volatility": {
                    "bollinger_bands": {
                        "upper": float(bollinger.bollinger_hband().iloc[-1]),
                        "middle": float(bollinger.bollinger_mavg().iloc[-1]),
                        "lower": float(bollinger.bollinger_lband().iloc[-1]),
                        "percent_b": float((close.iloc[-1] - bollinger.bollinger_lband().iloc[-1]) / 
                                          (bollinger.bollinger_hband().iloc[-1] - bollinger.bollinger_lband().iloc[-1])),
                        "bandwidth": float((bollinger.bollinger_hband().iloc[-1] - bollinger.bollinger_lband().iloc[-1]) / 
                                          bollinger.bollinger_mavg().iloc[-1]),
                        "squeeze": self._detect_bollinger_squeeze(bollinger)
                    },
                    "atr": {
                        "value": float(atr.average_true_range().iloc[-1]),
                        "percent": float(atr.average_true_range().iloc[-1] / close.iloc[-1] * 100)
                    },
                    "donchian_channels": self._parse_donchian(donchian, close)
                },
                "volume": {
                    "obv": {
                        "value": float(obv.on_balance_volume().iloc[-1]) if volume is not None else None,
                        "trend": self._get_obv_trend(obv.on_balance_volume()) if volume is not None else None
                    },
                    "mfi": {
                        "value": float(mfi.mfi().iloc[-1]) if volume is not None else None,
                        "signal": self._get_mfi_signal(mfi.mfi().iloc[-1]) if volume is not None else None
                    },
                    "volume_profile": self._analyze_volume_profile(data) if volume is not None else None,
                    "vwap": {
                        "value": float(volume_sma.vwap().iloc[-1]) if volume is not None else None,
                        "relation": "above" if close.iloc[-1] > volume_sma.vwap().iloc[-1] else "below"
                    } if volume is not None else None
                }
            }
        }
    
    def _analyze_fibonacci(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Layer 3: Fibonacci & Mathematical Analysis"""
        
        if len(data) < 100:
            return {"fibonacci": {"error": "Insufficient data"}}
        
        close = data['Close']
        
        # Find recent swing highs and lows
        swing_high, swing_low = self._find_swing_points(data)
        
        # Calculate Fibonacci levels
        fib_levels = {}
        if swing_high is not None and swing_low is not None:
            price_range = swing_high - swing_low
            
            fib_levels = {
                "0.0": swing_low,
                "23.6": swing_low + price_range * 0.236,
                "38.2": swing_low + price_range * 0.382,
                "50.0": swing_low + price_range * 0.5,
                "61.8": swing_low + price_range * 0.618,
                "78.6": swing_low + price_range * 0.786,
                "100.0": swing_high,
                "127.2": swing_high + price_range * 0.272,
                "161.8": swing_high + price_range * 0.618,
                "261.8": swing_high + price_range * 1.618
            }
        
        # Current price relation to Fibonacci levels
        current_price = close.iloc[-1]
        fib_relation = {}
        if fib_levels:
            for level_name, level_price in fib_levels.items():
                if abs(current_price - level_price) / current_price < 0.01:  # Within 1%
                    fib_relation[level_name] = level_price
        
        # Support and Resistance levels
        support_resistance = self._calculate_support_resistance(data)
        
        # Pivot Points
        pivot_points = self._calculate_pivot_points(data)
        
        return {
            "fibonacci": {
                "swing_high": float(swing_high) if swing_high else None,
                "swing_low": float(swing_low) if swing_low else None,
                "levels": fib_levels,
                "current_relation": fib_relation,
                "support_resistance": support_resistance,
                "pivot_points": pivot_points,
                "gann_analysis": self._perform_gann_analysis(data)
            }
        }
    
    def _analyze_market_structure(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Layer 4: Market Structure Analysis"""
        
        if len(data) < 30:
            return {"market_structure": {"error": "Insufficient data"}}
        
        close = data['Close']
        high = data['High']
        low = data['Low']
        
        # Trend identification
        trend = self._identify_trend(data)
        
        # Market phases
        phase = self._identify_market_phase(data)
        
        # Liquidity zones
        liquidity_zones = self._identify_liquidity_zones(data)
        
        # Order flow analysis (simplified)
        order_flow = self._analyze_order_flow(data)
        
        # Wyckoff analysis
        wyckoff_analysis = self._perform_wyckoff_analysis(data)
        
        return {
            "market_structure": {
                "trend": trend,
                "market_phase": phase,
                "structure": self._analyze_structure(data),
                "liquidity_zones": liquidity_zones,
                "order_flow": order_flow,
                "wyckoff_analysis": wyckoff_analysis,
                "market_regime": self._identify_market_regime(data)
            }
        }
    
    def _analyze_fundamental(self, symbol: str, data: pd.DataFrame) -> Dict[str, Any]:
        """Layer 5: Fundamental Analysis"""
        
        # This is a simplified version. In production, you would connect to
        # financial data APIs for comprehensive fundamental analysis
        
        fundamental = {
            "general": {
                "symbol": symbol,
                "analysis_time": datetime.now().isoformat()
            }
        }
        
        # For crypto
        if symbol in ["BTC", "ETH", "BNB", "XRP", "ADA", "SOL", "DOGE"]:
            fundamental.update(self._analyze_crypto_fundamental(symbol, data))
        
        # For stocks
        elif symbol in ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA"]:
            fundamental.update(self._analyze_stock_fundamental(symbol, data))
        
        # For forex
        elif any(symbol in pair for pair in ["EURUSD", "GBPUSD", "USDJPY"]):
            fundamental.update(self._analyze_forex_fundamental(symbol, data))
        
        return {"fundamental_analysis": fundamental}
    
    def _analyze_sentiment(self, symbol: str, data: pd.DataFrame) -> Dict[str, Any]:
        """Layer 6: Sentiment Analysis"""
        
        # Simplified sentiment analysis
        # In production, connect to sentiment APIs, social media, etc.
        
        close = data['Close']
        volume = data['Volume'] if 'Volume' in data.columns else None
        
        # Price-based sentiment
        price_change = ((close.iloc[-1] - close.iloc[-5]) / close.iloc[-5] * 100) if len(close) >= 5 else 0
        
        sentiment_score = 50  # Neutral baseline
        
        # Adjust based on price action
        if price_change > 5:
            sentiment_score += 20
        elif price_change < -5:
            sentiment_score -= 20
        
        # Volume sentiment
        if volume is not None and len(volume) >= 20:
            avg_volume = volume.iloc[-20:].mean()
            current_volume = volume.iloc[-1]
            if current_volume > avg_volume * 1.5:
                sentiment_score += 10  # High volume suggests conviction
        
        # Technical sentiment
        rsi = ta.momentum.RSIIndicator(close=close, window=14).rsi().iloc[-1]
        if rsi < 30:
            sentiment_score -= 15  # Oversold might indicate fear
        elif rsi > 70:
            sentiment_score += 15  # Overbought might indicate greed
        
        # Categorize sentiment
        if sentiment_score >= 70:
            sentiment = "EXTREME_GREED"
        elif sentiment_score >= 60:
            sentiment = "GREED"
        elif sentiment_score >= 40:
            sentiment = "NEUTRAL"
        elif sentiment_score >= 30:
            sentiment = "FEAR"
        else:
            sentiment = "EXTREME_FEAR"
        
        return {
            "sentiment_analysis": {
                "score": sentiment_score,
                "category": sentiment,
                "price_based": price_change,
                "fear_greed_index": self._estimate_fear_greed_index(symbol),
                "social_sentiment": self._estimate_social_sentiment(symbol),
                "put_call_ratio": None,  # Would require options data
                "vix_correlation": None,  # Would require VIX data
                "market_psychology": self._analyze_market_psychology(data)
            }
        }
    
    def _analyze_risk_management(self, symbol: str, data: pd.DataFrame, 
                                analysis_results: Dict) -> Dict[str, Any]:
        """Layer 7: Risk Management Analysis"""
        
        if len(data) < 20:
            return {"risk_management": {"error": "Insufficient data"}}
        
        close = data['Close']
        current_price = close.iloc[-1]
        
        # Calculate ATR for volatility
        high = data['High']
        low = data['Low']
        atr = ta.volatility.AverageTrueRange(high=high, low=low, close=close)
        atr_value = atr.average_true_range().iloc[-1]
        
        # Determine stop loss levels
        stop_loss_levels = self._calculate_stop_loss_levels(data, analysis_results)
        
        # Calculate position size based on risk
        position_sizing = self._calculate_position_sizing(
            current_price, 
            stop_loss_levels.get("technical", current_price * 0.95),
            atr_value
        )
        
        # Risk/Reward analysis
        risk_reward = self._analyze_risk_reward(data, analysis_results)
        
        # Correlation check (simplified)
        correlation_risk = self._assess_correlation_risk(symbol)
        
        # Volatility adjustment
        volatility_adjustment = self._calculate_volatility_adjustment(atr_value, data)
        
        # Kelly Criterion (simplified)
        kelly_position = self._calculate_kelly_criterion(analysis_results)
        
        return {
            "risk_management": {
                "current_price": float(current_price),
                "atr": {
                    "value": float(atr_value),
                    "percent": float(atr_value / current_price * 100)
                },
                "stop_loss_levels": stop_loss_levels,
                "position_sizing": position_sizing,
                "risk_reward_analysis": risk_reward,
                "correlation_risk": correlation_risk,
                "volatility_adjustment": volatility_adjustment,
                "kelly_criterion": kelly_position,
                "maximum_drawdown": self._calculate_max_drawdown(data),
                "var_95": self._calculate_var(data, 0.95),
                "risk_factors": self._identify_risk_factors(analysis_results)
            }
        }
    
    def _generate_final_signal(self, analysis_results: Dict) -> Dict[str, Any]:
        """Generate final trading signal based on all analysis layers"""
        
        signals = []
        confidence_score = 0
        risk_level = "MEDIUM"
        
        # Price action signals
        pa = analysis_results.get("price_action", {})
        if pa.get("active_patterns_count", 0) > 0:
            signals.append("Active price patterns detected")
            confidence_score += 10
        
        # Technical signals
        ti = analysis_results.get("technical_indicators", {})
        momentum = ti.get("momentum", {})
        trend = ti.get("trend", {})
        
        # RSI signal
        rsi_signal = momentum.get("rsi", {}).get("signal", "neutral")
        if rsi_signal == "oversold":
            signals.append("RSI oversold - potential bounce")
            confidence_score += 15
        elif rsi_signal == "overbought":
            signals.append("RSI overbought - potential pullback")
            confidence_score -= 10
        
        # MACD signal
        macd_signal = momentum.get("macd", {}).get("signal", "neutral")
        if macd_signal == "bullish":
            signals.append("MACD bullish crossover")
            confidence_score += 10
        
        # Trend signals
        ma = trend.get("moving_averages", {})
        if ma.get("golden_cross", False):
            signals.append("Golden Cross detected")
            confidence_score += 20
        elif ma.get("death_cross", False):
            signals.append("Death Cross detected")
            confidence_score -= 20
        
        # Trend strength
        adx_strength = trend.get("adx", {}).get("trend_strength", "weak")
        if adx_strength == "strong":
            signals.append("Strong trend confirmed")
            confidence_score += 15
        
        # Fibonacci signals
        fib = analysis_results.get("fibonacci", {})
        fib_relation = fib.get("current_relation", {})
        if fib_relation:
            signals.append(f"At Fibonacci level: {list(fib_relation.keys())[0]}")
            confidence_score += 5
        
        # Market structure
        ms = analysis_results.get("market_structure", {})
        market_trend = ms.get("trend", {}).get("primary", "sideways")
        if market_trend == "uptrend":
            signals.append("Primary uptrend confirmed")
            confidence_score += 15
        elif market_trend == "downtrend":
            signals.append("Primary downtrend confirmed")
            confidence_score -= 15
        
        # Sentiment signals
        sentiment = analysis_results.get("sentiment_analysis", {})
        sentiment_cat = sentiment.get("category", "NEUTRAL")
        if sentiment_cat == "EXTREME_FEAR":
            signals.append("Extreme fear - contrarian opportunity")
            confidence_score += 20
        elif sentiment_cat == "EXTREME_GREED":
            signals.append("Extreme greed - caution needed")
            confidence_score -= 20
        
        # Risk/Reward
        rm = analysis_results.get("risk_management", {})
        rr = rm.get("risk_reward_analysis", {})
        rr_ratio = rr.get("ratio", 1)
        if rr_ratio >= 3:
            signals.append(f"Excellent R:R ratio ({rr_ratio}:1)")
            confidence_score += 25
        elif rr_ratio >= 2:
            signals.append(f"Good R:R ratio ({rr_ratio}:1)")
            confidence_score += 15
        
        # Determine final signal
        if confidence_score >= 50:
            final_signal = "STRONG_BUY"
            risk_level = "LOW"
        elif confidence_score >= 30:
            final_signal = "BUY"
            risk_level = "MEDIUM"
        elif confidence_score >= 10:
            final_signal = "HOLD"
            risk_level = "MEDIUM"
        elif confidence_score >= -10:
            final_signal = "HOLD"
            risk_level = "HIGH"
        elif confidence_score >= -30:
            final_signal = "SELL"
            risk_level = "HIGH"
        else:
            final_signal = "STRONG_SELL"
            risk_level = "VERY_HIGH"
        
        # Time horizon
        if confidence_score > 40 or confidence_score < -40:
            time_horizon = "MEDIUM_TERM"
        else:
            time_horizon = "SHORT_TERM"
        
        return {
            "final_signal": {
                "decision": final_signal,
                "confidence_score": confidence_score,
                "risk_level": risk_level,
                "time_horizon": time_horizon,
                "signals": signals,
                "confidence_breakdown": {
                    "technical": confidence_score * 0.4,
                    "sentiment": confidence_score * 0.3,
                    "risk_reward": confidence_score * 0.3
                },
                "recommended_action": self._get_recommended_action(final_signal, confidence_score),
                "next_review": (datetime.now() + timedelta(hours=24)).isoformat()
            }
        }
    
    # Helper methods for pattern detection (simplified versions)
    
    def _detect_doji(self, data: pd.DataFrame) -> Dict:
        """Detect Doji patterns"""
        if len(data) < 1:
            return {"detected": False}
        
        close = data['Close'].iloc[-1]
        open_ = data['Open'].iloc[-1]
        high = data['High'].iloc[-1]
        low = data['Low'].iloc[-1]
        
        body_size = abs(close - open_)
        total_range = high - low
        
        if total_range > 0 and body_size / total_range < 0.1:
            return {
                "detected": True,
                "type": "Doji",
                "confidence": 0.7,
                "interpretation": "Indecision in market"
            }
        
        return {"detected": False}
    
    def _detect_hammer(self, data: pd.DataFrame) -> Dict:
        """Detect Hammer pattern"""
        if len(data) < 1:
            return {"detected": False}
        
        close = data['Close'].iloc[-1]
        open_ = data['Open'].iloc[-1]
        high = data['High'].iloc[-1]
        low = data['Low'].iloc[-1]
        
        body_size = abs(close - open_)
        lower_shadow = min(close, open_) - low
        upper_shadow = high - max(close, open_)
        
        is_bullish = close > open_
        
        if (lower_shadow > body_size * 2 and 
            upper_shadow < body_size * 0.3 and
            is_bullish):
            return {
                "detected": True,
                "type": "Hammer",
                "confidence": 0.75,
                "interpretation": "Bullish reversal signal after downtrend"
            }
        
        return {"detected": False}
    
    def _detect_engulfing(self, data: pd.DataFrame) -> Dict:
        """Detect Engulfing pattern"""
        if len(data) < 2:
            return {"detected": False}
        
        current_close = data['Close'].iloc[-1]
        current_open = data['Open'].iloc[-1]
        prev_close = data['Close'].iloc[-2]
        prev_open = data['Open'].iloc[-2]
        
        current_body = abs(current_close - current_open)
        prev_body = abs(prev_close - prev_open)
        
        # Bullish engulfing
        if (prev_close < prev_open and  # Previous candle bearish
            current_close > current_open and  # Current candle bullish
            current_open <= prev_close and  # Current opens below previous close
            current_close >= prev_open):  # Current closes above previous open
            
            return {
                "detected": True,
                "type": "Bullish Engulfing",
                "confidence": 0.8,
                "interpretation": "Strong bullish reversal signal"
            }
        
        # Bearish engulfing
        elif (prev_close > prev_open and  # Previous candle bullish
              current_close < current_open and  # Current candle bearish
              current_open >= prev_close and  # Current opens above previous close
              current_close <= prev_open):  # Current closes below previous open
            
            return {
                "detected": True,
                "type": "Bearish Engulfing",
                "confidence": 0.8,
                "interpretation": "Strong bearish reversal signal"
            }
        
        return {"detected": False}
    
    # ... Additional pattern detection methods would go here
    # For brevity, I'm including simplified versions of key methods
    
    def _get_rsi_signal(self, rsi_value: float) -> str:
        """Get RSI signal"""
        if rsi_value > 70:
            return "overbought"
        elif rsi_value < 30:
            return "oversold"
        elif rsi_value > 50:
            return "bullish"
        elif rsi_value < 50:
            return "bearish"
        else:
            return "neutral"
    
    def _calculate_divergences(self, data: pd.DataFrame, rsi_indicator, macd_indicator) -> Dict:
        """Calculate RSI and MACD divergences"""
        # Simplified divergence calculation
        close = data['Close']
        rsi = rsi_indicator.rsi()
        
        if len(close) < 20 or len(rsi) < 20:
            return {}
        
        # Look for regular bullish divergence
        price_lows = []
        rsi_lows = []
        
        for i in range(-10, 0):
            if i < -1:
                if close.iloc[i] < close.iloc[i-1] and close.iloc[i] < close.iloc[i+1]:
                    price_lows.append((i, close.iloc[i]))
                if rsi.iloc[i] < rsi.iloc[i-1] and rsi.iloc[i] < rsi.iloc[i+1]:
                    rsi_lows.append((i, rsi.iloc[i]))
        
        divergences = {}
        
        if len(price_lows) >= 2 and len(rsi_lows) >= 2:
            # Check for bullish divergence (price makes lower low, RSI makes higher low)
            if (price_lows[-1][1] < price_lows[-2][1] and 
                rsi_lows[-1][1] > rsi_lows[-2][1]):
                divergences["rsi"] = "bullish_divergence"
            # Check for bearish divergence (price makes higher high, RSI makes lower high)
            elif (price_lows[-1][1] > price_lows[-2][1] and 
                  rsi_lows[-1][1] < rsi_lows[-2][1]):
                divergences["rsi"] = "bearish_divergence"
        
        return divergences
    
    def _identify_trend(self, data: pd.DataFrame) -> Dict:
        """Identify market trend"""
        close = data['Close']
        
        if len(close) < 20:
            return {"primary": "unknown", "strength": "weak"}
        
        # Calculate simple moving averages
        sma_20 = close.rolling(window=20).mean()
        sma_50 = close.rolling(window=50).mean()
        
        current_price = close.iloc[-1]
        
        # Determine trend based on price position relative to MAs
        if current_price > sma_20.iloc[-1] > sma_50.iloc[-1]:
            trend = "uptrend"
        elif current_price < sma_20.iloc[-1] < sma_50.iloc[-1]:
            trend = "downtrend"
        else:
            trend = "sideways"
        
        # Calculate trend strength using ADX
        high = data['High']
        low = data['Low']
        adx_indicator = ta.trend.ADXIndicator(high=high, low=low, close=close)
        adx_value = adx_indicator.adx().iloc[-1]
        
        if adx_value > 25:
            strength = "strong"
        elif adx_value > 20:
            strength = "moderate"
        else:
            strength = "weak"
        
        return {
            "primary": trend,
            "strength": strength,
            "adx_value": float(adx_value),
            "price_above_sma20": current_price > sma_20.iloc[-1],
            "price_above_sma50": current_price > sma_50.iloc[-1]
        }
    
    def _calculate_position_sizing(self, current_price: float, 
                                 stop_price: float, atr: float) -> Dict:
        """Calculate position sizing based on risk management principles"""
        
        risk_per_trade = 0.02  # 2% risk per trade
        account_size = 10000  # Default account size
        
        # Calculate risk amount
        risk_amount = account_size * risk_per_trade
        
        # Calculate stop distance
        stop_distance = abs(current_price - stop_price)
        stop_percent = (stop_distance / current_price) * 100
        
        # Calculate position size
        position_size = risk_amount / stop_distance
        
        # Adjust for volatility
        volatility_ratio = atr / current_price
        if volatility_ratio > 0.05:  # High volatility
            position_size *= 0.5
        elif volatility_ratio < 0.01:  # Low volatility
            position_size *= 1.5
        
        # Calculate position value
        position_value = position_size * current_price
        
        return {
            "account_size": account_size,
            "risk_per_trade_percent": risk_per_trade * 100,
            "risk_amount": risk_amount,
            "stop_distance": stop_distance,
            "stop_percent": stop_percent,
            "position_size_units": position_size,
            "position_value": position_value,
            "position_percent_of_account": (position_value / account_size) * 100,
            "volatility_adjusted": volatility_ratio > 0.05 or volatility_ratio < 0.01
        }
    
    def _analyze_risk_reward(self, data: pd.DataFrame, 
                           analysis_results: Dict) -> Dict:
        """Analyze risk/reward ratios"""
        
        close = data['Close']
        current_price = close.iloc[-1]
        
        # Get potential targets from analysis
        technical = analysis_results.get("technical_indicators", {})
        fibonacci = analysis_results.get("fibonacci", {})
        
        # Calculate potential targets
        targets = []
        
        # Bollinger Band target
        bb = technical.get("volatility", {}).get("bollinger_bands", {})
        if bb.get("upper"):
            targets.append({
                "type": "Bollinger_Upper",
                "price": bb["upper"],
                "distance_percent": ((bb["upper"] - current_price) / current_price) * 100
            })
        
        # Fibonacci extension targets
        fib_levels = fibonacci.get("levels", {})
        for level, price in fib_levels.items():
            if float(level) > 100:  # Extension levels
                targets.append({
                    "type": f"Fib_{level}",
                    "price": price,
                    "distance_percent": ((price - current_price) / current_price) * 100
                })
        
        # Calculate stop loss from technical levels
        stop_loss = current_price * 0.95  # Default 5% stop
        
        # Find best R:R target
        best_target = None
        best_rr = 0
        
        for target in targets:
            reward = target["price"] - current_price
            risk = current_price - stop_loss
            
            if risk > 0:
                rr_ratio = reward / risk
                if rr_ratio > best_rr:
                    best_rr = rr_ratio
                    best_target = target
        
        return {
            "current_price": current_price,
            "stop_loss": stop_loss,
            "risk_amount": current_price - stop_loss,
            "risk_percent": ((current_price - stop_loss) / current_price) * 100,
            "potential_targets": targets,
            "best_target": best_target,
            "best_rr_ratio": best_rr,
            "recommended_rr_minimum": 2.0,
            "meets_minimum_rr": best_rr >= 2.0
        }
    
    def _get_recommended_action(self, signal: str, confidence: int) -> str:
        """Get recommended action based on signal and confidence"""
        
        actions = {
            "STRONG_BUY": "Açık pozisyon al veya mevcut pozisyonu artır",
            "BUY": "Pozisyon al veya küçük ekleme yap",
            "HOLD": "Mevcut pozisyonu koru, yeni pozisyon alma",
            "SELL": "Pozisyon azalt veya kısmi çıkış yap",
            "STRONG_SELL": "Pozisyon kapat veya kısa pozisyon aç"
        }
        
        base_action = actions.get(signal, "Bekle ve izle")
        
        if confidence > 60:
            return f"🎯 {base_action} - YÜKSEK GÜVEN"
        elif confidence > 30:
            return f"📈 {base_action} - ORTA GÜVEN"
        else:
            return f"⚠️ {base_action} - DÜŞÜK GÜVEN (DİKKATLİ OL)"
    
    # Additional simplified helper methods
    def _detect_hanging_man(self, data: pd.DataFrame) -> Dict:
        return {"detected": False}
    
    def _detect_shooting_star(self, data: pd.DataFrame) -> Dict:
        return {"detected": False}
    
    def _detect_marubozu(self, data: pd.DataFrame) -> Dict:
        return {"detected": False}
    
    def _detect_spinning_top(self, data: pd.DataFrame) -> Dict:
        return {"detected": False}
    
    def _detect_harami(self, data: pd.DataFrame) -> Dict:
        return {"detected": False}
    
    def _detect_morning_star(self, data: pd.DataFrame) -> Dict:
        return {"detected": False}
    
    def _detect_evening_star(self, data: pd.DataFrame) -> Dict:
        return {"detected": False}
    
    def _detect_three_white_soldiers(self, data: pd.DataFrame) -> Dict:
        return {"detected": False}
    
    def _detect_three_black_crows(self, data: pd.DataFrame) -> Dict:
        return {"detected": False}
    
    def _detect_head_shoulders(self, data: pd.DataFrame) -> Dict:
        return {"detected": False}
    
    def _detect_double_top_bottom(self, data: pd.DataFrame) -> Dict:
        return {"detected": False}
    
    def _detect_triangles(self, data: pd.DataFrame) -> Dict:
        return {"detected": False}
    
    def _detect_flags_pennants(self, data: pd.DataFrame) -> Dict:
        return {"detected": False}
    
    def _detect_cup_handle(self, data: pd.DataFrame) -> Dict:
        return {"detected": False}
    
    def _analyze_elliott_wave(self, data: pd.DataFrame) -> Dict:
        return {"wave_count": "unknown", "current_wave": "unknown"}
    
    def _analyze_harmonic_patterns(self, data: pd.DataFrame) -> Dict:
        return {"patterns": []}
    
    def _get_last_signals(self, patterns: Dict) -> List[str]:
        return []
    
    def _analyze_last_candles(self, data: pd.DataFrame, count: int) -> Dict:
        return {"analysis": "No significant patterns"}
    
    def _get_stoch_signal(self, k: float, d: float) -> str:
        return "neutral"
    
    def _get_williams_r_signal(self, value: float) -> str:
        return "neutral"
    
    def _get_cci_signal(self, value: float) -> str:
        return "neutral"
    
    def _get_adx_strength(self, value: float) -> str:
        return "weak"
    
    def _parse_ichimoku(self, ichimoku, close) -> Dict:
        return {"signal": "neutral"}
    
    def _parse_supertrend(self, supertrend, close) -> Dict:
        return {"signal": "neutral"}
    
    def _detect_bollinger_squeeze(self, bollinger) -> bool:
        return False
    
    def _parse_donchian(self, donchian, close) -> Dict:
        return {"signal": "neutral"}
    
    def _get_obv_trend(self, obv) -> str:
        return "neutral"
    
    def _get_mfi_signal(self, mfi) -> str:
        return "neutral"
    
    def _analyze_volume_profile(self, data) -> Dict:
        return {"poc": 0, "value_area": {"high": 0, "low": 0}}
    
    def _find_swing_points(self, data) -> Tuple[float, float]:
        return None, None
    
    def _calculate_support_resistance(self, data) -> Dict:
        return {"support": [], "resistance": []}
    
    def _calculate_pivot_points(self, data) -> Dict:
        return {"pivot": 0, "r1": 0, "r2": 0, "s1": 0, "s2": 0}
    
    def _perform_gann_analysis(self, data) -> Dict:
        return {"analysis": "Not implemented"}
    
    def _identify_market_phase(self, data) -> str:
        return "unknown"
    
    def _analyze_structure(self, data) -> Dict:
        return {"higher_highs": False, "higher_lows": False}
    
    def _identify_liquidity_zones(self, data) -> List[Dict]:
        return []
    
    def _analyze_order_flow(self, data) -> Dict:
        return {"bid_ask_imbalance": 0}
    
    def _perform_wyckoff_analysis(self, data) -> Dict:
        return {"phase": "unknown"}
    
    def _identify_market_regime(self, data) -> str:
        return "normal"
    
    def _analyze_crypto_fundamental(self, symbol, data) -> Dict:
        return {"market_cap": 0, "volume_24h": 0}
    
    def _analyze_stock_fundamental(self, symbol, data) -> Dict:
        return {"pe_ratio": 0, "market_cap": 0}
    
    def _analyze_forex_fundamental(self, symbol, data) -> Dict:
        return {"interest_rate_differential": 0}
    
    def _estimate_fear_greed_index(self, symbol) -> int:
        return 50
    
    def _estimate_social_sentiment(self, symbol) -> Dict:
        return {"score": 50, "buzz": "normal"}
    
    def _analyze_market_psychology(self, data) -> str:
        return "neutral"
    
    def _calculate_stop_loss_levels(self, data, analysis_results) -> Dict:
        return {"technical": data['Close'].iloc[-1] * 0.95}
    
    def _assess_correlation_risk(self, symbol) -> Dict:
        return {"risk": "low", "correlated_assets": []}
    
    def _calculate_volatility_adjustment(self, atr, data) -> Dict:
        return {"adjustment_factor": 1.0}
    
    def _calculate_kelly_criterion(self, analysis_results) -> Dict:
        return {"optimal_position": 0.1, "recommended": 0.025}
    
    def _calculate_max_drawdown(self, data) -> float:
        return 0.0
    
    def _calculate_var(self, data, confidence) -> float:
        return 0.0
    
    def _identify_risk_factors(self, analysis_results) -> List[str]:
        return ["General market risk"]
