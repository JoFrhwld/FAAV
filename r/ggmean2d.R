StatMean2d <- proto(Stat,
	{
		required_aes <- c("x", "y")
		default_geom <- function(.) GeomPoint
		objname <- "mean2d"

		calculate_groups <- function(., data, scales, ...){
			.super$calculate_groups(., data, scales,...)
		}
		calculate <- function(., data, scales, level = 0.75, segments = 51,...){
			data.frame(x = mean(data$x), y = mean(data$y))
		}
	}
)

stat_mean2d <- StatMean2d$build_accessor()
